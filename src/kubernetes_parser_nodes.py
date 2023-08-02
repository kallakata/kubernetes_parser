"""
    This class retrieves the list of the cluster's nodes.
    It uses the kubernetes Python client to list the nodes, authenticating
    using the present kube context.
"""

import argparse
import time
import sys
from auth import AuthNodes
from prettytable import PrettyTable
from googleapiclient.discovery import build

class NodeList:
    def __init__(self, context=False, cluster=None, project_id=None, zone=None, auth=[]):
        self.auth = auth
        self.context = context
        self.cluster = cluster
        self.project_id = project_id
        self.zone = zone

    def list_nodes(self):
        if self.context is None:
            raise Exception("Context is missing.")

        print('Listing nodes on',
                f'namespace {self.context}')
        time.sleep(2)
        print("Listing running nodes...")
        not_running_nodes = []
        nodes_list = self.auth.get()
        if len(nodes_list.items) > 0:
            time.sleep(2)
            names = []
            runtime = []
            os = []
            ips = []
            for node in nodes_list.items:
                names.append(node.metadata.name)
                runtime.append(node.status.node_info.os_image)
                ips.append(node.spec.pod_cidr)
                os.append("/".join([node.status.node_info.operating_system, node.status.node_info.architecture]))
            t = PrettyTable()
            t.add_column('Name', names)
            t.add_column('Runtime', runtime)
            t.add_column('OS', os)
            t.add_column('IP', ips)
            print(t)

        else:
            print("No nodes in context, please choose a different one.")

    def list_nodes_in_pool(self):
        """Lists all clusters and associated node pools."""
        service = build("container", "v1")
        clusters_resource = service.projects().zones().clusters()

        clusters_response = clusters_resource.list(
            projectId=self.project_id, zone=self.zone
        ).execute()
        # t = PrettyTable()
        # names_cluster = []
        # status_cluster = []
        # version_cluster = []
        # names_nodepool = []
        # status_nodepool = []
        # config_nodepool = []

        for cluster in clusters_response.get("clusters", []):
            print(
                "Cluster: {}, Status: {}, Current Master Version: {}".format(
                    cluster["name"], cluster["status"], cluster["currentMasterVersion"]
                )
            )
            # t.add_column('Cluster', cluster["name"])
            # t.add_column('Cluster status', cluster["status"])
            # names_cluster.append(cluster["name"])
            # status_cluster.append(cluster["status"])
            # version_cluster.append(cluster["currentMasterVersion"])

            nodepools_response = (
                clusters_resource.nodePools()
                .list(projectId=self.project_id, zone=self.zone, clusterId=self.cluster)
                .execute()
            )

            # t.add_column('Cluster name', names_cluster)
            # t.add_column('Cluster status', status_cluster)
            # t.add_column('Version', version_cluster)
            # print(t)

            for nodepool in nodepools_response["nodePools"]:
                print(
                    "\n-> Pool: {},\n  Status: {},\n  Machine Type: {},\n "
                    " Autoscaling: {},\n  MinNodeCount: {},\n  MaxNodeCount: {}".format(
                        nodepool["name"],
                        nodepool["status"],
                        nodepool["config"]["machineType"],
                        nodepool.get("autoscaling", {}).get("enabled", False),
                        nodepool.get("autoscaling", {}).get("minNodeCount"),
                        nodepool.get("autoscaling", {}).get("maxNodeCount")
                    )
                )
        return []

if __name__ == '__main__':
    try:
        """Command-line prompts."""
        parser = argparse.ArgumentParser(prog='parse_nodes',
                                        usage='nodes [context]',
                                        description=__doc__,
                                        formatter_class=argparse.RawDescriptionHelpFormatter)
        parser.add_argument("--context",
            help='The context for kubernetes cluster.',
            action='store',
            default=None,
            dest="context",
            # nargs='?'
        )
        parser.add_argument("--cluster",
            help='Cluster to list the nodes in.',
            action='store',
            default=None,
            dest="cluster",
            nargs='?'
        )
        parser.add_argument("--project_id",
            help='Project ID instead of context.',
            action='store',
            default=None,
            dest="project_id",
            nargs='?'
        )
        parser.add_argument("--zone",
            help='Zone to list nodepools in. Serves as a replacement for --context in combination with --project_id',
            action='store',
            default=None,
            dest="zone",
            nargs='?'
        )
        parser.add_argument("--limit",
            help='Maximum number of pods to list.',
            dest="limit",
            required=False
        )
        parser.add_argument("--timeout_seconds",
            help='Timeout in seconds.',
            dest="timeout_seconds",
            nargs="?",
            type=int,
            required=False
        )
        parser.add_argument("--watch",
            help='True or false... watch.',
            action='store_true',
            required=False
        )

        arguments = parser.parse_args()

        # if arguments.context is None:
        #     parser.error("'Context' is required.")

        auth = AuthNodes(auth_method='local', context=arguments.context)

        if all(item is None for item in [arguments.cluster, arguments.project_id, arguments.zone]) and arguments.context is not None:
            list_nodes = NodeList(arguments.context, arguments.cluster, arguments.project_id, arguments.zone, auth)
            list_nodes.list_nodes()

        elif all(item is not None for item in [arguments.cluster, arguments.project_id, arguments.zone]) and arguments.context is None:
            list_nodes = NodeList(arguments.context, arguments.cluster, arguments.project_id, arguments.zone, auth)
            list_nodes.list_nodes_in_pool()

        else:
            sys.tracebacklimit = 0
            raise Exception("Context, project ID or zone is missing.\nTo list nodepools and clusters, specify project and zone. To list nodes, specify context.")
            parser.print_help()

    except KeyboardInterrupt:
        print('Aborted.')
        sys.exit(2)

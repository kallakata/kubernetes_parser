"""
    This class retrieves the list of the cluster's nodes and nodepools.
    It uses the kubernetes Python client to list the nodes, authenticating
    using the present kube context.
"""

import argparse
import time
import sys
from auth import AuthNodes
from prettytable import PrettyTable
from googleapiclient.discovery import build
from prompt_toolkit import prompt
from prompt_completer import Completer

class UltimateHelpFormatter(
    argparse.RawTextHelpFormatter, argparse.ArgumentDefaultsHelpFormatter
):
    pass

class NodeList:
    def __init__(self, context=False, auth=[]):
        self.auth = auth
        self.context = context

    def list_nodes(self):
        if self.context is None:
            raise Exception("Context is missing.")

        print('Listing nodes in',
                f'context {self.context}')
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
    
class PoolList:
    def __init__(self, cluster=None, project_id=None, zone=None, auth=[]):
        self.auth = auth
        self.cluster = cluster
        self.project_id = project_id
        self.zone = zone

    def list_nodes_in_pool(self):
        """Lists all clusters and associated node pools."""
        service = build("container", "v1")
        clusters_resource = service.projects().zones().clusters()

        clusters_response = clusters_resource.list(
            projectId=self.project_id, zone=self.zone
        ).execute()

        t = PrettyTable()
        p = PrettyTable()
        names_cluster, status_cluster, version_cluster, names_nodepool, status_nodepool, version_nodepool, mtype_nodepool, asc_enabled, asc_min, asc_max = ([] for i in range(10))

        print(
            "Listing clusters..."
            )

        for cluster in clusters_response.get("clusters", []):

            # names_cluster.append(cluster["name"])
            # status_cluster.append(cluster["status"])
            # version_cluster.append(cluster["currentMasterVersion"])

            if self.cluster is None:
                nodepools_response = (
                    clusters_resource.nodePools()
                    .list(projectId=self.project_id, zone=self.zone, clusterId=cluster["name"])
                    .execute()
                )
                names_cluster.append(cluster["name"])
                status_cluster.append(cluster["status"])
                version_cluster.append(cluster["currentMasterVersion"])
            else:
                nodepools_response = (
                    clusters_resource.nodePools()
                    .list(projectId=self.project_id, zone=self.zone, clusterId=self.cluster)
                    .execute()
                )
                names_cluster.append(cluster["name"])
                status_cluster.append(cluster["status"])
                version_cluster.append(cluster["currentMasterVersion"])

        t.add_column('Cluster', names_cluster)
        t.add_column('Cluster status', status_cluster)
        t.add_column('Cluster version', version_cluster)

        print(t)

        print("Listing nodepools...")

        for nodepool in nodepools_response["nodePools"]:

            names_nodepool.append(nodepool["name"])
            status_nodepool.append(nodepool["status"])
            version_nodepool.append(nodepool["version"])
            mtype_nodepool.append(nodepool["config"]["machineType"])
            asc_enabled.append(nodepool.get("autoscaling", {}).get("enabled", False))
            asc_min.append(nodepool.get("autoscaling", {}).get("minNodeCount"))
            asc_max.append(nodepool.get("autoscaling", {}).get("maxNodeCount"))

        p.add_column('Nodepool', names_nodepool)
        p.add_column('Status', status_nodepool)
        p.add_column('Version', version_nodepool)
        p.add_column('mType', mtype_nodepool)
        p.add_column('Autoscaling', asc_enabled)
        p.add_column('MinNode', asc_min)
        p.add_column('MaxNode', asc_max)
        print(p)

        return []

if __name__ == '__main__':
    try:
        """Command-line prompts."""
        parser = argparse.ArgumentParser(prog='Kubernetes parser',
                                        usage='nodes [command]',
                                        description=__doc__,
                                        formatter_class=UltimateHelpFormatter)
        subparsers = parser.add_subparsers(dest='command')
        subparsers.required = True

        # List-nodes command
        lnodes = subparsers.add_parser('list_nodes', help='List nodes in context.', formatter_class=UltimateHelpFormatter)
        lnodes.add_argument("--context", "-c",
            help='The context for kubernetes cluster.',
            action='store',
            default=None,   
            dest="context",
            # nargs='?'
        )
        # lnodes.add_argument("--cluster",
        #     help='Cluster to list the nodes in.',
        #     action='store',
        #     default=None,
        #     dest="cluster",
        #     nargs='?'
        # )
        # lnodes.add_argument("--project_id",
        #     help='Project ID instead of context.',
        #     action='store',
        #     default=None,
        #     dest="project_id",
        #     nargs='?'
        # )
        # lnodes.add_argument("--zone",
        #     help='Zone to list nodepools in. Serves as a replacement for --context in combination with --project_id',
        #     action='store',
        #     default=None,
        #     dest="zone",
        #     nargs='?'
        # )
        lnodes.add_argument("--limit",
            help='Maximum number of pods to list.',
            dest="limit",
            required=False
        )
        lnodes.add_argument("--timeout_seconds",
            help='Timeout in seconds.',
            dest="timeout_seconds",
            nargs="?",
            type=int,
            required=False
        )
        lnodes.add_argument("--watch",
            help='True or false... watch.',
            action='store_true',
            required=False
        )

        # List-nodepools command
        lpools = subparsers.add_parser('list_nodepools', help='List nodepools and clusters in project and zone.', formatter_class=UltimateHelpFormatter)
        lpools.add_argument("--cluster", "-c",
            help='Cluster to list the nodes in.',
            action='store',
            default=None,
            dest="cluster",
            nargs='?'
        )
        # lpools.add_argument("--context",
        #     help='The context for kubernetes cluster.',
        #     action='store',
        #     default=None,
        #     dest="context",
        #     # nargs='?'
        # )
        lpools.add_argument("--project_id", "-p",
            help='Project ID instead of context.',
            action='store',
            default=None,
            dest="project_id",
            nargs='?'
        )
        lpools.add_argument("--zone", "-z",
            help='Zone to list nodepools in. Serves as a replacement for --context in combination with --project_id',
            action='store',
            default=None,
            dest="zone",
            nargs='?'
        )
        lpools.add_argument("--limit", "-l",
            help='Maximum number of pods to list.',
            dest="limit",
            required=False
        )
        lpools.add_argument("--timeout_seconds", "-t",
            help='Timeout in seconds.',
            dest="timeout_seconds",
            nargs="?",
            type=int,
            required=False
        )
        lpools.add_argument("--watch", "-w",
            help='True or false... watch.',
            action='store_true',
            required=False
        )

        arguments = parser.parse_args()
        completer = Completer()

        # if arguments.context is None:
        #     parser.error("'Context' is required.")

        if arguments.command == 'list_nodes':
            # if all(item is None for item in [arguments.cluster, arguments.project_id, arguments.zone]) and arguments.context is not None:
            if arguments.context is None:
                sys.tracebacklimit = 0
                raise Exception("Please specify context.")

            auth = AuthNodes(auth_method='local', context=arguments.context)
            list_nodes = NodeList(arguments.context, auth)
            p = prompt("Do you want to continue? \n", completer=completer.zoneCompleter(), complete_while_typing=True)
            if p == "Yes" or p == "Y":
                time.sleep(1)
                print("\nProceeding...\n")
                time.sleep(2)
                list_nodes.list_nodes()
            else:
                print('Aborted')
                sys.exit(1)

        elif arguments.command == 'list_nodepools':
            # elif all(item is not None for item in [arguments.cluster, arguments.project_id, arguments.zone]) and arguments.context is None:
            if any(item is None for item in [arguments.project_id, arguments.zone]):
                sys.tracebacklimit = 0
                raise Exception("Please specify project_id, zone and cluster.")
            
            list_nodepools = PoolList(arguments.cluster, arguments.project_id, arguments.zone)
            p = prompt("Do you want to continue? ", completer=completer.zoneCompleter(), complete_while_typing=True)
            if p == "Yes" or p == "Y":
                time.sleep(1)
                print("\nProceeding...\n")
                time.sleep(2)
                list_nodepools.list_nodes_in_pool()
            else:
                print('Aborted')
                sys.exit(1)

        elif arguments.command is None:
            sys.tracebacklimit = 0
            raise Exception("Please specify command: 1) list_nodes, 2) list_nodepools")
            lpools.print_help()

    except KeyboardInterrupt:
        print('Aborted.')
        sys.exit(2)

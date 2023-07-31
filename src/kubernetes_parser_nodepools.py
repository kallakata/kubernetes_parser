"""
    This class retrieves the list of the cluster's nodepools.
    It uses the kubernetes Python client to list the nodepools, authenticating
    using the present kube context.
"""

import argparse
import time
import sys
from prettytable import PrettyTable
from googleapiclient.discovery import build

class NodepoolsList:
    def __init__(self, project_id=None, zone=None):
        self.project_id = project_id
        self.zone = zone

    def list_clusters_and_nodepools(self):
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
                .list(projectId=self.project_id, zone=self.zone, clusterId=cluster["name"])
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
                # names_nodepool.append(nodepool["name"])
                # status_nodepool.append(nodepool["status"])
                # config_nodepool.append(nodepool["config"]["machineType"])
            # t.add_column('Nodepool', names_nodepool)
            # t.add_column('Nodepool status', status_nodepool)
            # t.add_column('Config', config_nodepool)
            # print(t)


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(
            description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
        )
        subparsers = parser.add_subparsers(dest="command")
        list_clusters_and_nodepools_parser = subparsers.add_parser(
            "list_clusters_and_nodepools", help=NodepoolsList.list_clusters_and_nodepools.__doc__
        )
        list_clusters_and_nodepools_parser.add_argument("--project_id")
        list_clusters_and_nodepools_parser.add_argument("--zone")

        args = parser.parse_args()

        if args.command == "list_clusters_and_nodepools":
            listing = NodepoolsList(project_id=args.project_id, zone=args.zone)
            listing.list_clusters_and_nodepools()
        else:
            parser.print_help()

    except KeyboardInterrupt:
        print('Aborted.')
        sys.exit(2)

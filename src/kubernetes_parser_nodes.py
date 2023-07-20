"""
    This class retrieves the list of the cluster's nodes.
    It uses the kubernetes Python client to list the nodes, authenticating
    using the present kube context.
"""

from kubernetes import client, config
import argparse

class NodeList:
    def list_nodes(context):
        config.load_kube_config(context=context)

        kube_client = client.CoreV1Api()
        node_list = kube_client.list_node(watch=False, pretty=True, limit=1000)
        if len(node_list.items) > 0:
            print("NODE\t\t\t\t\t\tSTATUS")
            for node in node_list.items:
                node_name = node.metadata.name
                node_status = "Not Ready"   # Unknown, not ready, unhealthy, etc.
                node_scheduling = node.spec.unschedulable
                for condition in node.status.conditions:
                    if condition.type == "Ready" and condition.status:
                        node_status = "Ready"
                        break
                if node_scheduling is None or not node_scheduling:
                    print(f"{node_name} {node_status}")
                else:
                    print(f"{node_name} {node_status},SchedulingDisabled")
        else:
            print("No nodes available in the cluster")

    if __name__ == '__main__':
        """List nodes."""
        parser = argparse.ArgumentParser(description='List nodes for context.')
        parser.add_argument("--context",
            help='The kubeconfig context to list nodes in.',
            dest="context"
        )

        arguments = parser.parse_args()

        if arguments.context is None:
            parser.error("A 'context' is required.")

        list_nodes(arguments.context)


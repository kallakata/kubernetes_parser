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

class NodeList:
    def __init__(self, context=False, auth=[]):
        self.auth = auth
        self.context = context

    def list_nodes(self):
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

        # for resp in response.__dict__.items():
        #     resp = list(resp)
        #     if resp.status.reason == "Terminated" or resp.status.phase == "Failed":
        #         print("Listing defunct pods...")
        #         # print("\t\tPOD\t\t\tSTATUS\t\t\tIP\t\t\tREASON")
        #         time.sleep(2)
        #         print(f"The {pod.metadata.name} status is non-running because of: {reason}")
        #     else:
        #         print("Listing running pods...")
        #         print("\t\tPOD\t\t\tSTATUS\t\t\tIP\t\t\tREASON")
        #         print("%s\t\t%s\t\t\t%s" % (pod.metadata.name,
        #                             pod.status.phase,
        #                             pod.status.pod_ip))
        #         print("\t\t\t\t\t\t\t\t\t\t\t%s" % (response.status.reason))
        return []

if __name__ == '__main__':
    try:
        """Command-line prompts."""
        parser = argparse.ArgumentParser(prog='parse_nodes',
                                        usage='nodes [context]',
                                        description='Returns the list of nodes in given context.')
        parser.add_argument("--context",
            help='The context for kubernetes cluster.',
            action='store',
            default=False,
            dest="context",
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

        if arguments.context is None:
            parser.error("'Context' is required.")

        auth = AuthNodes(auth_method='local', context=arguments.context)
        listing = NodeList(arguments.context, auth)
        listing.list_nodes()

    except KeyboardInterrupt:
        print('Aborted.')
        sys.exit(2)

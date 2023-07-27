"""
    This class retrieves the list of the cluster's pods.
    It uses the kubernetes Python client to list the pods, authenticating
    using the present kube context.
"""

import argparse
import time
import sys
from auth import AuthPods
from prettytable import PrettyTable

class PodsList:
    def __init__(self, namespace=False, context=False, auth=[]):
        self.namespace = namespace
        self.auth = auth
        self.context = context

    def list_pods(self):
        print('Listing pods on',
                f'namespace {self.namespace} and context {self.context}' if self.namespace\
                else 'all namespaces')
        time.sleep(2)
        print("Listing running pods...")
        not_running_containers = []
        pods_list = self.auth.get()
        if len(pods_list.items) > 0:
            time.sleep(2)
            names = []
            states = []
            ips = []
            node = []
            for pod in pods_list.items:
                names.append(pod.metadata.name)
                states.append(pod.status.phase)
                ips.append(pod.status.pod_ip)
                node.append(pod.spec.node_name)
            t = PrettyTable()
            t.add_column('Name', names)
            t.add_column('State', states)
            t.add_column('IP', ips)
            t.add_column('Node', node)
            print(t)
            # if pod.status.phase.lower() == 'running':
            #     print(f"Pod {pod.metadata.name} on {self.namespace} is running...")
            #     print("\t\tPOD\t\t\tSTATUS\t\t\tIP\t\t\tREASON")
            #     print("%s\t\t%s\t\t\t%s" % (pod.metadata.name,
            #                         pod.status.phase,
            #                         pod.status.pod_ip))
            #     print("\t\t\t\t\t\t\t\t\t\t\t%s" % (pod.status.reason))
            # else:
            #     terminated = not_running_containers.append(pod.metadata.name)
            #     print(f"Pod {pod.metadata.name} in {self.namespace} has a status of: {pod.status.phase}")
            #     print(terminated)

        else:
            print("No pods in namespace, please choose a different one.")

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
        parser = argparse.ArgumentParser(prog='parse_pods',
                                        usage='pods [namespace] [context]',
                                        description='Returns the list of pods in given namespace and context.')
        parser.add_argument("--namespace",
            help='The namespace to list pods in.',
            action='store',
            default=False,
            nargs='?',
            dest="namespace"
        )
        parser.add_argument("--context",
            help='The context for kubernetes cluster.',
            action='store',
            default=False,
            nargs='?',
            dest="context"
        )
        parser.add_argument("--limit",
            help='Maximum number of pods to list.',
            dest="limit",
            required=False
        )
        parser.add_argument("--timeout_seconds",
            help='Timeout.',
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

        if arguments.context is None or arguments.namespace is None:
            parser.error("'Context' or 'namespace' is required.")

        # add context option, not current one
        auth = AuthPods(auth_method='local', namespace=arguments.namespace, context=arguments.context)
        listing = PodsList(arguments.namespace, arguments.context, auth)
        listing.list_pods()

    except KeyboardInterrupt:
        print('Aborted.')
        sys.exit(2)
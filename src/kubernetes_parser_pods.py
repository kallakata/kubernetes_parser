"""
    This class retrieves the list of the cluster's pods.
    It uses the kubernetes Python client to list the pods, authenticating
    using the present kube context.
"""

import argparse
import time
import sys
from auth import AuthPods

class PodsList:
    def __init__(self, namespace=False, auth=[], context=False, **kwargs):
        self.namespace = namespace
        self.auth = auth

    def list_pods(self, context, namespace):
        print('Listing pods with restarting containers on',
                f'namespace {self.namespace}' if self.namespace\
                else 'all namespaces')

        not_running_containers = []
        pods_list = self.auth.pod_list()
        if len(pods_list.items) > 0:
            time.sleep(2)
            for pod in pods_list.items:
                if pod.status.phase.lower() == 'running':
                    print(f"Pod {pod} on {self.namespace} is running...")
                    print("\t\tPOD\t\t\tSTATUS\t\t\tIP\t\t\tREASON")
                    print("%s\t\t%s\t\t\t%s" % (pod.metadata.name,
                                        pod.status.phase,
                                        pod.status.pod_ip))
                    print("\t\t\t\t\t\t\t\t\t\t\t%s" % (pod.status.reason))
                else:
                    terminated = not_running_containers.append(pod.metadata.name)
                    print(f"Pod {pod} in {self.namespace} has a status of: {pod.status.phase}")
                    print(terminated)

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

if __name__ == '__main__':
    try:
        """List pods in a namespace."""
        parser = argparse.ArgumentParser(description='List pods in a namespace.')
        parser.add_argument("--namespace",
            help='The namespace to list pods in.',
            dest="namespace",
            required=False
        )
        parser.add_argument("--context",
            help='The context for kubernetes cluster.',
            dest="context",
            required=False
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

        final = AuthPods(context=arguments.context, namespace=arguments.namespace)
        listing = PodsList(arguments.namespace, arguments.context)
    except KeyboardInterrupt:
        print('Aborted.')
        sys.exit(2)
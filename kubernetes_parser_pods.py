#!/usr/bin/env python

from kubernetes import client, config
import argparse
import time

def list_pods(context, namespace, timeout_seconds, watch, limit):
    config.load_kube_config(context=context)

    kube_client = client.CoreV1Api()
    pod_list = kube_client.list_namespaced_pod(namespace, pretty=True, timeout_seconds=timeout_seconds, watch=watch, limit=limit)

    if len(pod_list.items) > 0:
        time.sleep(2)
        for pod in pod_list.items:
            # pod_name = pod.metadata.name
            # condition = pod.status.phase
            # if condition == "Pending" or condition == "Failed":
            #     print(f"{pod_name} not running, condition is: {condition}")
            # else:
            response = kube_client.read_namespaced_pod(name=pod.metadata.name, namespace=namespace, pretty=True)
            reason = response.status.reason
            phase = response.status.phase
            if reason == "Terminated" or phase == "Failed":
                print("Listing defunct pods...")
                # print("\t\tPOD\t\t\tSTATUS\t\t\tIP\t\t\tREASON")
                time.sleep(2)
                print(f"The {pod.metadata.name} status is non-running because of: {reason}")
            else:
                print("Listing running pods...")
                print("\t\tPOD\t\t\tSTATUS\t\t\tIP\t\t\tREASON")
                print("%s\t\t%s\t\t\t%s" % (pod.metadata.name,
                                    pod.status.phase,
                                    pod.status.pod_ip))
                print("\t\t\t\t\t\t\t\t\t\t\t%s" % (response.status.reason))

    else:
        print("No pods in namespace, please choose a different one.")

if __name__ == '__main__':
    """List pods in a namespace."""
    parser = argparse.ArgumentParser(description='List pods in a namespace.')
    parser.add_argument("--namespace",
        help='The namespace to list pods in.',
        dest="namespace"
    )
    parser.add_argument("--context",
        help='The context for kubernetes cluster.',
        dest="context"
    )
    parser.add_argument("--limit",
        help='Maximum number of pods to list.',
        dest="limit"
    )
    parser.add_argument("--timeout_seconds",
        help='Timeout.',
        dest="timeout_seconds",
        nargs="?",
        type=int
    )
    parser.add_argument("--watch",
        help='True or false... watch.',
        dest="watch"
    )

    arguments = parser.parse_args()

    if arguments.context is None or arguments.namespace is None:
        parser.error("A 'context', 'namespace' and 'limit' is required.")

    list_pods(arguments.context, arguments.namespace, arguments.limit, arguments.timeout_seconds, arguments.watch)
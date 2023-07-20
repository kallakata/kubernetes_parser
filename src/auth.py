"""
    This class authenticates to the cluster and retrieves required information based on the prompt.
"""
import sys
from kubernetes import client, config
from kubernetes.client.rest import ApiException

class AuthPods:
    def __init__(self, auth_method="local", namespace=None, context=None):
        self.namespace = namespace
        if auth_method == 'local':
            config.load_kube_config()
        self.context = context

    def pod_list(self):
        """
            Returns the pods list on the specified namespace. If not set, list pods for
            all namespaces.
        """
        kube_client = client.CoreV1Api()

        try:
            if self.context:
                return kube_client.list_namespaced_pod(self.context, self.limit)
            if self.namespace:
                return kube_client.list_namespaced_pod(self.namespace, self.limit)
            return kube_client.list_pod_for_all_namespaces()
        except Exception as exception:
            print('There was an error while listing: ')
            print(exception.reason)
            sys.exit(1)

class AuthNodes:
    def __init__(self, auth_method="local", namespace=None, context=None):
        self.namespace = namespace
        if auth_method == 'local':
            config.load_kube_config()
        self.context = context
        # self.limit = limit
        # self.timeout_seconds = timeout_seconds

    def node_list(self):
        """
            Returns the nodes list on the specified namespace. If not set, list pods for
            all namespaces.
        """
        kube_client = client.CoreV1Api()
        try:
            return kube_client.list_node(watch=False, pretty=True, limit=1000)
        except ApiException as exception:
            print('There was an error while listing: ')
            print(exception.reason)
            sys.exit(1)
"""
    This class authenticates to the cluster and retrieves required information based on the prompt.
"""
import sys
from kubernetes import client, config
from kubernetes.client.rest import Exception

class Auth:
    def __init__(self, auth_method="local", namespace=None):
        self.namespace = namespace
        if auth_method == 'local':
            config.load_kube_config()

    def list(self):
        """
            Returns the pods or nodes list on the specified namespace. If not set, list pods for
            all namespaces.
        """
        kube_client = client.CoreV1Api()
        try:
            if self.namespace:
                return kube_client.list_namespaces(self.namespace)
            return kube_client.list_pod_for_all_namespaces()
        except Exception as exception:
            print('There was an error while listing: ')
            print(exception.reason)
            sys.exit(1)
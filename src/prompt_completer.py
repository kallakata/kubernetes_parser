from prompt_toolkit.completion import FuzzyWordCompleter
from prompt_toolkit.shortcuts import CompleteStyle, prompt
from prompt_toolkit.completion import NestedCompleter
from kubernetes import client, config
from kubernetes.client import configuration

class Completer:
    """
        This class offers the possibility to autocomplete prompts.
    """
    def __init__(self):
        self.__init__

    def projectCompleter(self):
        project_completer = FuzzyWordCompleter(
        [
            "alligator",
            "ant",
            "ape",
            "bat",
            "bear",
            "beaver",
            "bee",
            "bison",
            "butterfly",
            "cat",
            "chicken",
            "crocodile",
            "dinosaur",
            "dog",
            "dolphin",
            "dove",
            "duck",
            "eagle",
            "elephant",
            "fish",
            "goat",
            "gorilla",
            "kangaroo",
            "leopard",
            "lion",
            "mouse",
            "rabbit",
            "rat",
            "snake",
            "spider",
            "turkey",
            "turtle",
        ],
    )
        return project_completer

    def contextCompleter(self):
        contexts = config.list_kube_config_contexts()
        context_list = [context["name"] for context in contexts]
        for index in range(len(context_list)):
            # 0 bobby
            # 1 hadz
            # 2 com
            print(index, contexts[index])
        return index

    def zoneCompleter(self):
        zone_completer = FuzzyWordCompleter(
            [
                "Yes",
                "No"
            ],
        )
        return zone_completer

    def clusterCompleter(self):
        cluster_completer = FuzzyWordCompleter(
            [
                "alligator",
                "ant",
                "ape",
                "bat",
                "bear",
                "beaver",
                "bee",
                "bison",
                "butterfly",
                "cat",
                "chicken",
                "crocodile",
                "dinosaur",
                "dog",
                "dolphin",
                "dove",
                "duck",
                "eagle",
                "elephant",
                "fish",
                "goat",
                "gorilla",
                "kangaroo",
                "leopard",
                "lion",
                "mouse",
                "rabbit",
                "rat",
                "snake",
                "spider",
                "turkey",
                "turtle",
            ],
        )
        return cluster_completer


    def nestedCompleter(self):
        nested_completer = NestedCompleter.from_nested_dict(
        {
            "show": {"version": None, "clock": None, "ip": {"interface": {"brief": None}}},
            "exit": None,
        }
    )
        return nested_completer
    
    def namespaceCompleter(self):
        ns_completer = FuzzyWordCompleter(
            [
                "alligator",
                "ant",
                "ape",
                "bat",
                "bear",
                "beaver",
                "bee",
                "bison",
                "butterfly",
                "cat",
                "chicken",
                "crocodile",
                "dinosaur",
                "dog",
                "dolphin",
                "dove",
                "duck",
                "eagle",
                "elephant",
                "fish",
                "goat",
                "gorilla",
                "kangaroo",
                "leopard",
                "lion",
                "mouse",
                "rabbit",
                "rat",
                "snake",
                "spider",
                "turkey",
                "turtle",
            ],
        )
        return ns_completer
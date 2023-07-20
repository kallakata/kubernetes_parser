## Kubernetes parser ##

A simple parser to list nodes, pods, namespaces and metadata from a desired context, along with chosen sub-metadata in a cli-like manner.

Inspired by kubectl, serves for internal purposes and experiments.

Please check Makefile for additional options.

### Usage ###

```console
$ pip install -r requirements.txt
$ chmod +x kubernetes_parser_nodes.py kubernetes_parser_pods.py
$ ./kubernetes_parser_nodes.py [ARGUMENTS]
$ ./kubernetes_parser_pods.py --help
```

### Run pods CLI ###
```console
$ make setup-pods
```

### Install dependencies for pods CLI ###
```console
$ make install-pods
```

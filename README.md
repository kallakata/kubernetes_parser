## Kubernetes parser ##

A simple parser to list nodes, pods, namespaces and metadata from a desired context, along with chosen sub-metadata in a cli-like manner.

Inspired by kubectl, serves for internal purposes and experiments.

Please check Makefile or Kubernetes API docs (V1Pod and V1Node) for additional options.

## Usage ##

### Manual ###
```console
$ pip install -r requirements.txt
$ chmod +x kubernetes_parser_nodes.py kubernetes_parser_pods.py
$ ./kubernetes_parser_nodes.py [ARGUMENTS]
$ ./kubernetes_parser_pods.py --help
```

### Run pods CLI and install dependencies ###
```console
$ make install-pods
$ make setup-pods
$ pods [ARGUMENTS] --help
```

### Run nodes CLI and install dependencies ###
```console
$ make install-nodes
$ make setup-nodes
$ nodes [ARGUMENTS] --help
```

## Kubernetes parser ##

A simple parser to list nodes, pods, namespaces and metadata from a desired context, along with chosen sub-metadata in a cli-like manner.

Inspired by *kubectl*, serves for internal purposes and experiments. Later on, I would like to merge all three tools together. As of now, nodes and nodepool listing can be used conjoined.

Please check Makefile for additional options. Schema defined in Kubernetes API docs (V1Pod and V1Node)

## Usage ##

### Manual ###
```console
$ pip install -r requirements.txt
$ chmod +x kubernetes_parser_nodes.py kubernetes_parser_pods.py kubernetes_parser_nodepools.py
$ ./[PARSER] [ARGUMENTS]
$ ./[PARSER] --help
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

### Run nodepools CLI and install dependencies ###
```console
$ make install-nodepools
$ make setup-nodepools
$ nodepools [ARGUMENTS] --help
```

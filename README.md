## Kubernetes parser ##

A simple parser to list nodes, pods, namespaces and metadata from a desired context, along with chosen sub-metadata in a cli-like manner.

Inspired by *kubectl*, serves for internal purposes and experiments. Nodepool and nodes listing can be used in conjunction.

Please check Makefile for additional options. Schema defined in Kubernetes API docs (V1Pod and V1Node). Nodes-cli can be used both for nodepools and nodes, depending on the command.

## Usage ##

### Manual ###
```console
$ pip install -r requirements.txt
$ chmod +x kubernetes_parser_nodes.py kubernetes_parser_pods.py kubernetes_parser_nodepools.py
$ ./[PARSER] [COMMAND] [ARGUMENTS]
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
$ nodes [COMMANDS] [ARGUMENTS] --help
```

### Run nodepools CLI and install dependencies ###
```console
$ make install-nodepools
$ make setup-nodepools
$ nodepools [COMMANDS] [ARGUMENTS] --help
```

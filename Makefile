.PHONY: setup-pods
setup-pods:
	@which python3
	python3 -m pip install virtualenv
	python3 -m virtualenv pods-env
	./pods-env/bin/pip install -r requirements.txt

.PHONY: setup-nodes
setup-pods:
	@which python3
	python3 -m pip install virtualenv
	python3 -m virtualenv nodes-env
	./nodes-env/bin/pip install -r requirements.txt

.PHONY: install-pods
install-pods:
	@echo  "${PWD}/pods-env/bin/python3 ${PWD}/src/kubernetes_parser_pods.py \$$@" > pods
	@chmod +x pods
	@cp pods ${HOME}/bin/
	@echo "\nYou can add pods to your path running"
	@echo "$$ export PATH="\$${PATH}:\$${HOME}/bin""

.PHONY: install-nodes
install-nodes:
	@echo  "${PWD}/nodes-env/bin/python3 ${PWD}/src/kubernetes_parser_nodes.py \$$@" > nodes
	@chmod +x nodes
	@cp nodes ${HOME}/bin/
	@echo "\nYou can add nodes to your path running"
	@echo "$$ export PATH="\$${PATH}:\$${HOME}/bin""
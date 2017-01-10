DOCKER ?= $(shell which docker)
DOCKER_OPTIONS ?=

.PHONY: all bonobo push bash

all:
	DOCKER_OPTIONS=--no-cache make bonobo push

bonobo:
	$(DOCKER) pull python:3.6
	$(DOCKER) build $(DOCKER_OPTIONS) -t pybb/bonobo:3.6 .

push:
	$(DOCKER) push pybb/bonobo:3.6

bash:
	$(DOCKER) run -it --rm --user=bonobo pybb/bonobo:3.6 bash

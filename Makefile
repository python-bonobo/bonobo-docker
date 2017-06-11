# This file has been auto-generated.
# All changes will be lost, see Projectfile.
#
# Updated at 2017-06-11 10:29:13.160336

PACKAGE ?= bonobo_docker
PYTHON ?= $(shell which python)
PYTHON_BASENAME ?= $(shell basename $(PYTHON))
PYTHON_DIRNAME ?= $(shell dirname $(PYTHON))
PYTHON_REQUIREMENTS_FILE ?= requirements.txt
PYTHON_REQUIREMENTS_DEV_FILE ?= requirements-dev.txt
QUICK ?= 
PIP ?= $(PYTHON_DIRNAME)/pip
PIP_INSTALL_OPTIONS ?= 
PYTEST ?= $(PYTHON_DIRNAME)/pytest
PYTEST_OPTIONS ?= --capture=no --cov=$(PACKAGE) --cov-report html
SPHINX_BUILD ?= $(PYTHON_DIRNAME)/sphinx-build
SPHINX_OPTIONS ?= 
SPHINX_SOURCEDIR ?= docs
SPHINX_BUILDDIR ?= $(SPHINX_SOURCEDIR)/_build
YAPF ?= $(PYTHON_DIRNAME)/yapf
YAPF_OPTIONS ?= -rip
BONOBO_VERSION ?= $(shell bonobo version -qq)
VERSION ?= $(shell git describe 2>/dev/null || echo dev)

.PHONY: $(SPHINX_SOURCEDIR) clean format images install install-dev test

# Installs the local project dependencies.
install:
	if [ -z "$(QUICK)" ]; then \
	    $(PIP) install -U pip wheel $(PYTHON_PIP_INSTALL_OPTIONS) -r $(PYTHON_REQUIREMENTS_FILE) ; \
	fi

# Installs the local project dependencies, including development-only libraries.
install-dev:
	if [ -z "$(QUICK)" ]; then \
	    $(PIP) install -U pip wheel $(PYTHON_PIP_INSTALL_OPTIONS) -r $(PYTHON_REQUIREMENTS_DEV_FILE) ; \
	fi

# Cleans up the local mess.
clean:
	rm -rf build dist *.egg-info

test: install-dev
	$(PYTEST) $(PYTEST_OPTIONS) tests

$(SPHINX_SOURCEDIR): install-dev
	$(SPHINX_BUILD) -b html -D latex_paper_size=a4 $(SPHINX_OPTIONS) $(SPHINX_SOURCEDIR) $(SPHINX_BUILDDIR)/html

format: install-dev
	$(YAPF) $(YAPF_OPTIONS) .
	$(YAPF) $(YAPF_OPTIONS) Projectfile

# Build an pushes docker images.
images: install
	$(PYTHON) -m $(PACKAGE) build --version $(BONOBO_VERSION) --push

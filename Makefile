.ONESHELL:
.DEFAULT_GOAL := help
SHELL := /bin/bash

#virtual environment. If 0 issue warning
#Not activated:0
#activated: 1
ifeq ($(VIRTUAL_ENV),)
$(warning virtualenv not activated)
is_venv =
else
is_venv = 1
VENV_BIN := $(VIRTUAL_ENV)/bin
VENV_BIN_PYTHON := python3
PY_X_Y := $(shell $(VENV_BIN_PYTHON) -c 'import platform; t_ver = platform.python_version_tuple(); print(".".join(t_ver[:2]));')
endif

##@ Helpers

# https://www.thapaliya.com/en/writings/well-documented-makefiles/
.PHONY: help
help:					## (Default) Display this help -- Always up to date
	@awk -F ':.*##' '/^[^: ]+:.*##/{printf "  \033[1m%-20s\033[m %s\n",$$1,$$2} /^##@/{printf "\n%s\n",substr($$0,5)}' $(MAKEFILE_LIST)

##@ Testing

.PHONY: pre-commit
pre-commit: private target_tty = $(if $(show),1,0)
pre-commit:				## Run pre-commit checks -- make [show=1] pre-commit
ifeq ($(is_venv),1)
	@out=$$(PRE_COMMIT_COLOR=never pre-commit run --all-files ||:)
	if [[ $(target_tty) -eq 1 ]]; then
	echo "$$out" | tee /tmp/out.txt
	else
	echo "$$out" > /tmp/out.txt
	fi
endif

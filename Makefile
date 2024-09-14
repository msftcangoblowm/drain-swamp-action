.ONESHELL:
.DEFAULT_GOAL := help
SHELL := /bin/bash

##@ Helpers

# https://www.thapaliya.com/en/writings/well-documented-makefiles/
.PHONY: help
help:					## (Default) Display this help -- Always up to date
	@awk -F ':.*##' '/^[^: ]+:.*##/{printf "  \033[1m%-20s\033[m %s\n",$$1,$$2} /^##@/{printf "\n%s\n",substr($$0,5)}' $(MAKEFILE_LIST)

##@ Testing

.PHONY: pre-commit
pre-commit:				## Run checks found in .pre-commit-config.yaml
	@pre-commit run --all-files

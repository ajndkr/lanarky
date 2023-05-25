.PHONY: help tests pre-commit
help:	## shows this help message
	@echo "Usage:\n\tmake <target>"
	@echo "\nAvailable targets:"
	@awk 'BEGIN {FS = ":.*##"; } /^[$$()% a-zA-Z_-]+:.*?##/ \
	{ printf "\t\033[36m%-30s\033[0m %s\n", $$1, $$2 } /^##@/ \
	{ printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

tests:	## run unit tests with coverage
	poetry run pytest \
	--cov=lanarky --cov-report=term-missing:skip-covered \
	-p pytest_asyncio -v

coverage:	## run unit tests with coverage
	poetry run coveralls

pre-commit:	## run pre-commit hooks
	poetry run pre-commit run --all-files

build-docs:	## build documentation
	poetry run sphinx-autobuild -b html --host 0.0.0.0 --port 8000 docs docs/_build/html

clean-docs: ## clean documentation
	rm -rf docs/_build

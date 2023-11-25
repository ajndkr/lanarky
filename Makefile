.PHONY: help tests coverage pre-commit
help:			## shows this help message
	@echo "Usage:\n\tmake <target>"
	@echo "\nAvailable targets:"
	@awk 'BEGIN {FS = ":.*##"; } /^[$$()% a-zA-Z_-]+:.*?##/ \
	{ printf "\t\033[36m%-30s\033[0m %s\n", $$1, $$2 } /^##@/ \
	{ printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

tests:			## run unit tests with coverage
	poetry run pytest \
	--cov=lanarky --cov-report=term-missing:skip-covered \
	-p pytest_asyncio -v
	find . -type d -name '__pycache__' -exec rm -r {} +

coverage:		## run unit tests with coverage
	poetry run coveralls

pre-commit:		## run pre-commit hooks
	poetry run pre-commit run --all-files

bump:			## bump version
	@read -p "Enter version bump (patch|minor|major): " arg; \
	if [ "$$arg" != "patch" ] && [ "$$arg" != "minor" ] && [ "$$arg" != "major" ]; then \
		echo "Usage: make bump (patch|minor|major)"; \
		exit 1; \
	fi; \
	current_version=$$(poetry version -s); \
	poetry version $$arg; \
	new_version=$$(poetry version -s); \
	git add pyproject.toml; \
	git commit -m "bump(ver): $$current_version → $$new_version";

.PHONY: help validate validate-config validate-content validate-env serve build clean

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

validate: validate-config validate-content ## Run all validation checks

validate-config: ## Validate Hugo configuration
	@echo "Validating configuration..."
	@python3 scripts/validate_config.py

validate-content: ## Validate markdown content
	@echo "Validating content..."
	@python3 scripts/validate_content.py

validate-env: ## Check development environment setup
	@echo "Checking development environment..."
	@python3 scripts/validate_env.py

serve: ## Start Hugo development server
	@echo "Starting Hugo development server..."
	@hugo serve

build: validate ## Build the site (with validation)
	@echo "Building site..."
	@hugo --minify --gc --enableGitInfo --panicOnWarning

clean: ## Clean generated files
	@echo "Cleaning generated files..."
	@rm -rf public resources .hugo_build.lock

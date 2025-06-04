
.PHONY: setup start run test clean help

# Default target
help:
	@echo "Available targets:"
	@echo "  activate    - Activate the virtual project environment"
	@echo "  setup       - Setup the project (check and install dependencies)"
	@echo "  start       - Start the FastAPI server"
	@echo "  run         - Alias for start"
	@echo "  clean       - Clean temporary files"
	@echo "  help        - Show this help message"

# Check and activate virtual environment
activate:
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		if [ -d "venv" ]; then \
			echo "Virtual environment found. Activating..."; \
			. venv/bin/activate; \
			if [ -z "$$VIRTUAL_ENV" ]; then \
				echo "Failed to activate virtual environment."; \
				exit 1; \
			fi; \
		else \
			echo "Virtual environment not found. Creating..."; \
			python -m venv venv; \
			echo "Activating..."; \
			. venv/bin/activate; \
			if [ -z "$$VIRTUAL_ENV" ]; then \
				echo "Failed to activate virtual environment after creation."; \
				exit 1; \
			fi; \
		fi; \
	else \
		echo "Virtual environment already activated."; \
	fi

# Setup project
setup: activate
	@if [ -f check_dependencies.py ]; then \
		echo "Checking and installing dependencies..."; \
		python3 check_dependencies.py; \
	else \
		echo "check_dependencies.py not found, installing from requirements.txt"; \
		pip install -r app/requirements.txt; \
	fi
	@echo "Project setup completed"

# Start the service
start: setup
	@echo "Starting FastAPI server..."
	python3 main.py

# Alias for start
run: start

# Clean temporary files
clean:
	@echo "Cleaning temporary files..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@echo "Cleanup completed"


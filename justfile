# Install dependencies
install:
    poetry install

# Format code
format:
    poetry run black .
    poetry run ruff check . --fix

# Lint only
lint:
    poetry run ruff check .

# Run API
run-api:
    poetry run uvicorn services.api_service.main:app --reload

# Run tests
test:
    poetry run pytest

# Show available commands
default:
    just --list

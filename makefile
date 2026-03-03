install:
	poetry install

format:
	poetry run black .
	poetry run ruff check . --fix

lint:
	poetry run ruff check .

run-api:
	poetry run uvicorn services.api-service.main:app --reload

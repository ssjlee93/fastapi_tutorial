.PHONY: local setup-db docker pg

# Run the app locally (uv + Python)
local:
	make pg
	uv run fastapi dev app/main.py

# Setup the database locally
setup-db:
	createdb -U postgres -h localhost fastapi

# Run the app and Postgres via Docker Compose
docker:
	docker compose up --build -d

# Run an instance of postgres on docker
pg:
	@if docker ps -a --format '{{.Names}}' | grep -q '^pg$$'; then \
		echo "Container 'pg' already exists, starting it..."; \
		docker start pg; \
	else \
		echo "Creating new 'pg' container..."; \
		docker run --name pg -p 5432:5432 -e POSTGRES_PASSWORD=password -e POSTGRES_DB=fastapi -d postgres; \
	fi
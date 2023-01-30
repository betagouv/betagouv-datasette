install:
	poetry install

dev:
	poetry run datasette ./app

refresh_data:
	rm app/data.sqlite
	poetry run python scripts/refresh_data.py

deploy:
	poetry run datasette publish fly --app betagouv-datasette --metadata app/metadata.yml app/*.sqlite

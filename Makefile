server:
	docker-compose up

db:
	docker-compose up postgresdb

shell:
	docker-compose run web python manage.py shell

migration:
	docker-compose run web python manage.py makemigrations

migrate:
	docker-compose run web python manage.py migrate

su:
	docker-compose run web python manage.py createsuperuser


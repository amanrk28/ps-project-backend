server:
	docker-compose up -d

db:
	docker-compose up postgresdb

shell:
	docker-compose run app python manage.py shell

migration:
	docker-compose run app python manage.py makemigrations

migrate:
	docker-compose run app python manage.py migrate

su:
	docker-compose run app python manage.py createsuperuser

down:
	docker-compose down

start:
	docker-compose start

stop:
	docker-compose stop
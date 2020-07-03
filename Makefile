build:
	docker-compose build

up:
	docker-compose up -d web db

reload:
	docker-compose exec web touch /tmp/reload.trigger

bash:
	docker-compose run --rm web bash
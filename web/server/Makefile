fe:
	docker build -t frontend-ds317:latest ../client/
	docker run -p 8000:8000 frontend-ds317:latest

db:
	docker build -t database-ds317:latest .
	docker run --rm -p 5432:5432 --name db317 database-ds317:latest

psql:
	psql -h localhost -p 5432 -U docker recommender

pgadmin:
	docker run \
		--rm \
		-p 5050:80 \
		-e PGADMIN_DEFAULT_EMAIL=khanhpg5@gmail.com \
		-e PGADMIN_DEFAULT_PASSWORD=docker \
		dpage/pgadmin4

flask:
	FLASK_APP=src/app.py flask run

predict:
	./src/models/run.sh

zip:
	zip ./static/csv/csv.zip ./static/csv/*.csv

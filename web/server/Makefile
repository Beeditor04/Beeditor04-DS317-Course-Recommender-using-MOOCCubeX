db:
	docker build -t database-ds317:latest .
	docker run -p 5432:5432 database-ds317:latest

psql:
	psql -h localhost -p 5432 -U docker recommender

flask:
	FLASK_APP=src/app.py flask run

predict:
	../../models/run.sh

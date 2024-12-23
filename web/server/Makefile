fe:
	docker build -t frontend-ds317:latest ../client/
	docker run -p 5173:5173 frontend-ds317:latest

db:
	docker build -t database-ds317:latest .
	docker run -p 5432:5432 database-ds317:latest

psql:
	psql -h localhost -p 5432 -U docker recommender

flask:
	FLASK_APP=src/app.py flask run

predict:
	../../models/run.sh

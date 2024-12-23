import json

from flask import Flask, g
from flask_cors import CORS


import psycopg2
from psycopg2 import pool, extras

app = Flask(__name__)
CORS(app, supports_credentials=True)

pool = psycopg2.pool.SimpleConnectionPool(
    minconn=1,
    maxconn=8,
    dbname="recommender",
    user="docker",
    password="docker",
    host="localhost",
    port="5432"
)

@app.before_request
def get_db_connection():
    g.db_conn = pool.getconn()

@app.teardown_request
def release_db_connection(exception=None):
    """Release the connection back to the pool after handling the request."""
    pool.putconn(g.db_conn)


@app.route("/user/<id>", methods=['GET'])
def get_user(id: str):
    with g.db_conn.cursor(cursor_factory = extras.RealDictCursor) as cursor:
        cursor.execute('SELECT * FROM users WHERE id = %s;', (id, ))
        user = cursor.fetchone()

    return json.dumps(user)


@app.route("/course/<id>", methods=['GET'])
def get_course(id: str):
    with g.db_conn.cursor(cursor_factory = extras.RealDictCursor) as cursor:
        cursor.execute('''
            SELECT
                course.*,
                teacher.name AS teacher_name,
                school.name AS school_name
            FROM course

            JOIN course_teacher
            ON course.id = course_teacher.course_id
            JOIN teacher
            ON teacher.id = course_teacher.teacher_id

            JOIN course_school
            ON course.id = course_school.course_id
            JOIN school
            ON school.id = course_school.school_id

            WHERE course.id = %s;
        ''', (id, ))
        course = cursor.fetchone()

    return json.dumps(course)


@app.route("/rec/<id>", methods=['GET'])
def get_recommendation(id: str):
    return '''[
        "C_584313",
        "C_584314",
        "C_584315",
        "C_584316",
        "C_584317",
        "C_584318",
        "C_584319",
        "C_584320",
        "C_584321",
        "C_584322"
    ]'''


# @app.route("/add/<user_id>/<course_id>", methods=['POST'])
# def add_course(user_id, course_id):
#     update_course_for_user('../../../data/', user_id, course_id)


@app.route("/all_course", methods=['GET'])
def all_course():
    with g.db_conn.cursor() as cursor:
        cursor.execute('SELECT id FROM course;')
        courses = cursor.fetchall()

    return json.dumps([c[0] for c in courses])

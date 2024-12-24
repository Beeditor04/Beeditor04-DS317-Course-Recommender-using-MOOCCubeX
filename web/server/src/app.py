import json
import subprocess

from flask import Flask, g
from flask_cors import CORS
import psycopg2
from psycopg2 import pool, extras

import pandas as pd

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

user_id_to_remapped = pd.read_csv('static/map/user_list.txt', sep=' ') \
    .set_index('org_id')['remap_id'].to_dict()
remapped_to_course_id = pd.read_csv('static/map/item_list.txt', sep=' ') \
    .set_index('remap_id')['org_id'].to_dict()


@app.before_request
def get_db_connection():
    g.db_conn = pool.getconn()
    g.db_conn.autocommit = True


@app.teardown_request
def release_db_connection(exception=None):
    """Release the connection back to the pool after handling the request."""
    pool.putconn(g.db_conn)


@app.route("/user/<id>", methods=['GET'])
def get_user(id: str):
    with g.db_conn.cursor(cursor_factory = extras.RealDictCursor) as cursor:
        cursor.execute('SELECT * FROM users WHERE id = %s;', (id, ))
        user = cursor.fetchone()

    with g.db_conn.cursor() as cursor:
        cursor.execute('SELECT course_id FROM user_course WHERE user_id = %s;', (id, ))
        user['course'] = [c for course in cursor.fetchall() for c in course]

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

            LEFT JOIN course_teacher
            ON course.id = course_teacher.course_id
            LEFT JOIN teacher
            ON teacher.id = course_teacher.teacher_id

            LEFT JOIN course_school
            ON course.id = course_school.course_id
            LEFT JOIN school
            ON school.id = course_school.school_id

            WHERE course.id = %s;
        ''', (id, ))
        course = cursor.fetchone()

    return json.dumps(course)


@app.route("/rec/<id>", methods=['GET'])
def get_recommendation(id: str):
    remapped = user_id_to_remapped[id]
    output = subprocess.check_output(
        "./src/models/run.sh " +
        str(remapped) +
        " 2> /dev/null | tail | awk '{ print $3 }'",

        shell=True,
        universal_newlines=True
    )
    remapped_course = list(map(
        lambda id: remapped_to_course_id[int(id)],
        output.splitlines()
    ))

    return json.dumps(remapped_course)

@app.route("/all_course", methods=['GET'])
def all_course():
    with g.db_conn.cursor() as cursor:
        cursor.execute('SELECT id FROM course;')
        courses = cursor.fetchall()

    return json.dumps([c[0] for c in courses])

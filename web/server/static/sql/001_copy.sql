COPY users (id, name, course)
FROM '/docker-entrypoint-initdb.d/user.csv'
WITH (FORMAT csv);

COPY course (id, name, prerequisites, about, field, resource)
FROM '/docker-entrypoint-initdb.d/course.csv'
WITH (FORMAT csv);

COPY teacher (id, name)
FROM '/docker-entrypoint-initdb.d/teacher.csv'
WITH (FORMAT csv);

COPY school (id, name)
FROM '/docker-entrypoint-initdb.d/school.csv'
WITH (FORMAT csv);

COPY concept (id, name)
FROM '/docker-entrypoint-initdb.d/concept.csv'
WITH (FORMAT csv);

COPY course_teacher (course_id, teacher_id)
FROM '/docker-entrypoint-initdb.d/course-teacher.csv'
WITH (FORMAT csv);

COPY course_school (course_id, school_id)
FROM '/docker-entrypoint-initdb.d/course-school.csv'
WITH (FORMAT csv);

COPY course_concept (course_id, concept_id)
FROM '/docker-entrypoint-initdb.d/course-concept.csv'
WITH (FORMAT csv)

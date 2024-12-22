CREATE TABLE users (
    id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(256)
);

CREATE TABLE course (
    id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(256) NOT NULL,
    prerequisites TEXT,
    about TEXT,
    field JSON,
    resource JSON
);

CREATE TABLE teacher (
    id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(128)
);

CREATE TABLE school (
    id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(128)
);

CREATE TABLE concept (
    id VARCHAR(64) PRIMARY KEY,
    name TEXT
);

CREATE TABLE user_course (
    user_id VARCHAR(64),
    course_id VARCHAR(64),
    PRIMARY KEY (user_id, course_id),
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (course_id) REFERENCES course (id)
);

CREATE TABLE course_teacher (
    course_id VARCHAR(64),
    teacher_id VARCHAR(64),
    PRIMARY KEY (course_id, teacher_id),
    FOREIGN KEY (course_id) REFERENCES course (id),
    FOREIGN KEY (teacher_id) REFERENCES teacher (id)
);

CREATE TABLE course_school (
    course_id VARCHAR(64),
    school_id VARCHAR(64),
    PRIMARY KEY (course_id, school_id),
    FOREIGN KEY (course_id) REFERENCES course (id),
    FOREIGN KEY (school_id) REFERENCES school (id)
);

CREATE TABLE course_concept (
    course_id VARCHAR(64),
    concept_id VARCHAR(64),
    PRIMARY KEY (course_id, concept_id),
    FOREIGN KEY (course_id) REFERENCES course (id),
    FOREIGN KEY (concept_id) REFERENCES concept (id)
)

-- SQL script to populate the database.

-- Turning foreign key constraint check off for easily emptying tables.
PRAGMA foreign_keys = OFF;

-- uncomment below commands to delete exisiting previous data before adding new
DELETE FROM department;
DELETE FROM votes;
DELETE FROM rating;
DELETE FROM prof_sec;
DELETE FROM review;
DELETE FROM users;
DELETE FROM section;
DELETE FROM offers;
DELETE FROM professor;
DELETE FROM course;

-- Running command below to make sure foreign key constraint check is on.
PRAGMA foreign_keys = ON;


-- Adding departments
INSERT INTO department (dept_name, school) VALUES ('Computer Science', 'SSE');
INSERT INTO department (dept_name, school) VALUES ('Physics', 'SSE');
INSERT INTO department (dept_name, school) VALUES ('Biology', 'SSE');
INSERT INTO department (dept_name, school) VALUES ('Mathematics', 'SSE');
INSERT INTO department (dept_name, school) VALUES ('Electrical Engineering', 'SSE');
INSERT INTO department (dept_name, school) VALUES ('Accounting and Finance', 'SDSB');
INSERT INTO department (dept_name, school) VALUES ('Management Sciences', 'SDSB');
INSERT INTO department (dept_name, school) VALUES ('History', 'HSS');

-- Adding professors
INSERT INTO professor (name, position, dept_name, qualification) VALUES ('Alferd Brown','Associate Professor','Computer Science','PhD Computer Science');
INSERT INTO professor (name, position, dept_name, qualification) VALUES ('Andy Pavlo','Professor','Computer Science','PhD Database Systems');
INSERT INTO professor (name, position, dept_name, qualification) VALUES ('Babar Ali','Assistant Professor','Physics','PhD Quantum Theory');
INSERT INTO professor (name, position, dept_name, qualification) VALUES ('Mubashir Anwar','Assistant Professor','Mathematics','PhD Mathematics');
INSERT INTO professor (name, position, dept_name, qualification) VALUES ('Hira Jamshed','Associate Professor','Computer Science','PhD Computational Engineering');
INSERT INTO professor (name, position, dept_name, qualification) VALUES ('Haris Noor','Professor','Management Sciences','MBA');
INSERT INTO professor (name, position, dept_name, qualification) VALUES ('Bruce Wayne','Professor','Electrical Engineering','PhD Electronics');

-- Adding course
INSERT INTO course (course_name, level) VALUES ('Intro. to Computer Science', 'UG');
INSERT INTO course (course_name, level) VALUES ('Intro. to Programming', 'UG');
INSERT INTO course (course_name, level) VALUES ('Electrical Systems', 'UG');
INSERT INTO course (course_name, level) VALUES ('Databases', 'UG/G');
INSERT INTO course (course_name, level) VALUES ('Quantum Computing', 'G');
INSERT INTO course (course_name, level) VALUES ('Data Structures', 'UG');
INSERT INTO course (course_name, level) VALUES ('Probability', 'UG');
INSERT INTO course (course_name, level) VALUES ('Calculus', 'UG');
INSERT INTO course (course_name, level) VALUES ('Linear Algebra', 'UG');

-- Adding section
INSERT INTO section (course_name, semester, year) VALUES ('Intro. to Computer Science', 'Fall', 2019);
INSERT INTO section (course_name, semester, year) VALUES ('Intro. to Computer Science', 'Spring', 2019);
INSERT INTO section (course_name, semester, year) VALUES ('Databases', 'Fall', 2018);
INSERT INTO section (course_name, semester, year) VALUES ('Databases', 'Fall', 2019);
INSERT INTO section (course_name, semester, year) VALUES ('Databases', 'Fall', 2020);

-- Adding prof_sec
INSERT INTO prof_sec (prof_id, course_name, semester, year) VALUES (1, 'Intro. to Computer Science', 'Fall', 2019);
INSERT INTO prof_sec (prof_id, course_name, semester, year) VALUES (2, 'Intro. to Computer Science', 'Spring', 2019);
INSERT INTO prof_sec (prof_id, course_name, semester, year) VALUES (3, 'Intro. to Computer Science', 'Fall', 2020);
INSERT INTO prof_sec (prof_id, course_name, semester, year) VALUES (4, 'Intro. to Computer Science', 'Fall', 2020);
INSERT INTO prof_sec (prof_id, course_name, semester, year) VALUES (5, 'Quantum Computing', 'Spring', 2019);
INSERT INTO prof_sec (prof_id, course_name, semester, year) VALUES (6, 'Databases', 'Spring', 2020);
INSERT INTO prof_sec (prof_id, course_name, semester, year) VALUES (6, 'Calculus', 'Spring', 2020);

-- Adding offers
INSERT INTO offers (course_code, course_name, dept_name) VALUES ('CS100', 'Intro. to Computer Science', 'Computer Science');
INSERT INTO offers (course_code, course_name, dept_name) VALUES ('CS105', 'Intro. to Programming', 'Computer Science');
INSERT INTO offers (course_code, course_name, dept_name) VALUES ('MATH230', 'Probability', 'Mathematics');

-- Adding reviews
INSERT INTO review VALUES (1,1,'Test review.','2020-12-3',1,'Intro. to Computer Science','Fall',2019);
INSERT INTO review VALUES (6, 50,'Test review.', CURRENT_TIMESTAMP,6,'Databases','Spring',2020);

-- Adding ratings
-- INSERT INTO rating VALUES (1,4,5,3);
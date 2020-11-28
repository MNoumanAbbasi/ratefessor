-- Uncomment to delete exisiting tables and start fresh
PRAGMA foreign_keys = OFF;
DROP TABLE IF EXISTS professor;
DROP TABLE IF EXISTS section;
DROP TABLE IF EXISTS prof_sec;
DROP TABLE IF EXISTS department;
DROP TABLE IF EXISTS course;
DROP TABLE IF EXISTS offers;
DROP TABLE IF EXISTS rating;
DROP TABLE IF EXISTS review;
DROP TABLE IF EXISTS votes;
DROP TABLE IF EXISTS users;
PRAGMA foreign_keys = ON;


CREATE TABLE professor (
    prof_id INTEGER, 
    name TEXT not null, 
    position TEXT, 
    dept_name TEXT, 
    qualification TEXT, 
    primary key (prof_id), 
    foreign key (dept_name) references department on delete set null
); 

CREATE TABLE section (
    course_name TEXT,  
    semester varchar(6) check (semester in ('Fall', 'Spring', 'Summer')), 
    year numeric(4,0) check (year > 1980 and year < 2200), 
    primary key (course_name, semester, year), 
    foreign key (course_name) references course on delete cascade 
);

CREATE TABLE prof_sec (
    prof_id INTEGER, 
    course_name TEXT, 
    semester varchar(6), 
    year numeric(4,0),   
    primary key (prof_id, course_name, semester, year),
    foreign key (prof_id) references professor on delete cascade, 
    foreign key (course_name, semester, year) references section on delete cascade
);

CREATE TABLE department (
    dept_name TEXT, 
    school TEXT not null, 
    primary key (dept_name)
);

CREATE TABLE course (
    course_name TEXT, 
    level varchar(4) check (level in ('UG', 'G', 'UG/G')), 
    primary key (course_name) 
);

CREATE TABLE offers (
    course_code varchar(8), 
    course_name TEXT, 
    dept_name TEXT, 
    primary key (course_name, dept_name), 
    foreign key (course_name) references course on delete cascade 
    foreign key (dept_name) references department on delete cascade 
);

CREATE TABLE rating (
    review_id INTEGER, 
    workload INTEGER check (workload in (1,2,3,4,5)), 
    learning INTEGER check (learning in (1,2,3,4,5)), 
    grading INTEGER check (grading in (1,2,3,4,5)), 
    primary key (review_id), 
    foreign key (review_id) references review on delete cascade 
);

CREATE TABLE review (
    review_id INTEGER, 
    user_id INTEGER not null, 
    text TEXT not null, 
    date DATETIME, 
    prof_id INTEGER not null,
    course_name TEXT not null, 
    semester varchar(6), 
    year numeric(4,0), 
    primary key (review_id), 
    foreign key (prof_id, course_name, semester, year) references prof_sec on delete cascade
);

CREATE TABLE votes (
    review_id INTEGER, 
    user_id INTEGER, 
    vote INTEGER check (vote in (1, -1)), 
    primary key (review_id, user_id) 
    foreign key (review_id) references review on delete cascade, 
    foreign key (user_id) references users on delete cascade  
);

CREATE TABLE users(
    user_id INTEGER, 
    email TEXT, 
    pswd_hash TEXT, 
    role varchar(6) check (role in ('admin', 'normal')), 
    primary key (user_id) 
);
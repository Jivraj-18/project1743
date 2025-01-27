CREATE TABLE "User" (
  "user_id" integer PRIMARY KEY,
  "fs_uniquifier" varchar UNIQUE NOT NULL,
  "email" varchar UNIQUE NOT NULL
);

CREATE TABLE "Student" (
  "student_id" SERIAL PRIMARY KEY,
  "Student_name" integer NOT NULL,
  "enroll_date" timestamp,
  "current_level" varchar DEFAULT 'foundation',
  "dob" timestamp,
  "about_me" varchar,
  "phone" integer UNIQUE,
  "email" varchar UNIQUE NOT NULL
);

CREATE TABLE "Course" (
  "course_id" SERIAL PRIMARY KEY,
  "name" varchar NOT NULL,
  "description" varchar
);

CREATE TABLE "Instructor" (
  "instructor_id" SERIAL PRIMARY KEY,
  "name" varchar NOT NULL,
  "email" varchar UNIQUE NOT NULL
);

CREATE TABLE "Instructor_course" (
  "id" integer PRIMARY KEY,
  "course_id" integer,
  "instructor_id" integer
);

CREATE TABLE "Course_student" (
  "id" integer PRIMARY KEY,
  "student_id" integer,
  "course_id" integer
);

CREATE TABLE "Assignment" (
  "assignment_id" integer PRIMARY KEY,
  "category" varchar NOT NULL,
  "course_id" integer NOT NULL,
  "deadline" timestamp NOT NULL,
  "which_week" timestamp NOT NULL
);

CREATE TABLE "Question" (
  "question_id" integer PRIMARY KEY,
  "type" varchar NOT NULL,
  "assignment_id" integer NOT NULL,
  "question" varchar NOT NULL,
  "options" varchar,
  "correct_options" varchar NOT NULL,
  "marks" integer NOT NULL,
  "hints" varchar,
  "text_solution" varchar
);

CREATE TABLE "Assignment_student" (
  "id" integer PRIMARY KEY,
  "assignment_id" integer,
  "student_id" integer,
  "marks_answers" varchar NOT NULL
);

CREATE TABLE "Content" (
  "content_id" integer PRIMARY KEY,
  "course_id" integer NOT NULL,
  "content_type" varchar NOT NULL,
  "url" varchar UNIQUE,
  "transcript_url" varchar UNIQUE
);

CREATE TABLE "Role" (
  "role_id" integer PRIMARY KEY,
  "name" varchar UNIQUE NOT NULL,
  "description" varchar
);

CREATE TABLE "User_role" (
  "id" integer PRIMARY KEY,
  "role_id" integer NOT NULL,
  "user_id" integer NOT NULL
);

ALTER TABLE "User_role" ADD FOREIGN KEY ("role_id") REFERENCES "Role" ("role_id");

ALTER TABLE "User_role" ADD FOREIGN KEY ("user_id") REFERENCES "User" ("user_id");

ALTER TABLE "Instructor" ADD FOREIGN KEY ("email") REFERENCES "User" ("email");

ALTER TABLE "Student" ADD FOREIGN KEY ("email") REFERENCES "User" ("email");

ALTER TABLE "Course_student" ADD FOREIGN KEY ("student_id") REFERENCES "Student" ("student_id");

ALTER TABLE "Course_student" ADD FOREIGN KEY ("course_id") REFERENCES "Course" ("course_id");

ALTER TABLE "Instructor_course" ADD FOREIGN KEY ("course_id") REFERENCES "Course" ("course_id");

ALTER TABLE "Instructor_course" ADD FOREIGN KEY ("instructor_id") REFERENCES "Instructor" ("instructor_id");

ALTER TABLE "Content" ADD FOREIGN KEY ("course_id") REFERENCES "Course" ("course_id");

ALTER TABLE "Assignment" ADD FOREIGN KEY ("course_id") REFERENCES "Course" ("course_id");

ALTER TABLE "Assignment_student" ADD FOREIGN KEY ("assignment_id") REFERENCES "Assignment" ("assignment_id");

ALTER TABLE "Assignment_student" ADD FOREIGN KEY ("assignment_id") REFERENCES "Student" ("student_id");

ALTER TABLE "Question" ADD FOREIGN KEY ("assignment_id") REFERENCES "Assignment" ("assignment_id");

DROP TABLE IF EXISTS jobs;
DROP TABLE IF EXISTS company_location;
DROP TABLE IF EXISTS job_rating;
DROP TABLE IF EXISTS job_sector;
DROP TABLE IF EXISTS job_salary;
DROP TABLE IF EXISTS employees;



CREATE TABLE IF NOT EXISTS jobs (
	job_title varchar (500) NOT NULL,
	job_description varchar(max),
	company varchar,
	location varchar(max),
	source varchar(256)
);


CREATE TABLE IF NOT EXISTS company_location (
	company varchar NOT NULL,
	location varchar(max),
	city varchar(256),
	state varchar(256),
	country varchar(256)
);


CREATE TABLE IF NOT EXISTS job_rating (
	job_title varchar (500) NOT NULL,
	company varchar,
	rating float,
	max_rating int
);


CREATE TABLE IF NOT EXISTS job_sector (
	job_title varchar (500) NOT NULL,
	sector varchar(max)
);



CREATE TABLE IF NOT EXISTS job_salary (
	job_title varchar (500) NOT NULL,
	company varchar,
	estimated_salary varchar (256)
);


CREATE TABLE IF NOT EXISTS employees (
	person_id int NOT NULL,
	hobby varchar(256),
	open_source_contrib varchar(256),
	country varchar(256),
	student varchar(256),
	employment varchar(256),
	main_education varchar(256),
	development_area varchar(max),
	latest_job varchar,
	productive_hours varchar,
	gender varchar(256),
	age varchar(256)
);

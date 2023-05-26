CREATE TABLE prof (
	ssno VARCHAR(4) PRIMARY KEY,
	pname CHAR(20),
	office VARCHAR(20),
	age INTEGER,
	sex CHAR(6),
	speciality VARCHAR(20),
	dept_did VARCHAR(4),
	FOREIGN KEY (dept_did) REFERENCES dept (did));
CREATE TABLE dept (
	did  VARCHAR(4) PRIMARY KEY,
	dname VARCHAR(20),
	budget DECIMAL(8,2),
	num_majors INTEGER,
	chair_ssno VARCHAR(4));

INSERT INTO prof 
VALUES ('p131', 'Alies', 'BS Hall 122', 33, 'Female', 'Accounting', 'a123');
INSERT INTO prof 
VALUES ('p121', 'Jason', 'BS Hall 132', 41, 'Male', 'Finance', 'a123');
INSERT INTO prof 
VALUES ('p141', 'John', 'BS Hall 222', 50, 'Female', 'Marketing', 'a123');
INSERT INTO prof 
VALUES ('p111', 'Calvin', 'BS Hall 321', 31, 'Female', 'Management', 'a123');
INSERT INTO prof 
VALUES ('p151', 'Julidan', 'COS Hall 421', 53, 'Male', 'Network', 'a223');
INSERT INTO prof 
VALUES ('p161', 'Hopkins', 'COS Hall 423', 42, 'Female', 'Digital design', 'a223');
INSERT INTO prof 
VALUES ('p171', 'Ronald', 'COS Hall 435', 37, 'Male', 'Data structure', 'a223');
INSERT INTO prof
VALUES ('p181', 'Emy', 'MAT Hall 111', 28, 'Female', 'Linear algebra', 'a333');
INSERT INTO prof
VALUES ('p191', 'Morina', 'MAT Hall 142', 35, 'Female', 'Math modeling', 'a333');
INSERT INTO prof
VALUES ('p201', 'Eijah', 'PY Hall 122', 30, 'Male', 'General physics', 'a423');
INSERT INTO prof
VALUES ('p211', 'Robert', 'PY Hall 212', 58, 'Male', 'Modern physics', 'a423');
INSERT INTO prof
VALUES ('p212', 'Andy', 'PY Hall 324', 39, 'Female', 'Mechanics', 'a423');
INSERT INTO prof
VALUES ('p213', 'Andrew', 'PY Hall 320', 52, 'Male', 'Thermal physics', 'a423');

INSERT INTO dept
VALUES ('a123', 'Business', 2300.42, 4, 'p111');
INSERT INTO dept
VALUES ('a223', 'Computer Science', 3700, 3, 'p161');
INSERT INTO dept
VALUES ('a333', 'Mathmatics', 1800.42, 2, 'p181');
INSERT INTO dept
VALUES ('a423', 'Physics', 2800.12, 4, 'p211');

SELECT pname, age, office 
FROM prof
WHERE prof.sex = 'Female' AND prof.speciality = 'Accounting'; /*user-specified*/

Unclustered hash index on speciality and sex in Prof

SELECT *
FROM dept as dt, prof as pf
WHERE dt.did = pf.dept_did AND
pf.age > 45 AND pf.age < 55; /*user-specific*/

Clustered B+ tree index on dept_did and age in Prof. And unclustered hash index on did in Dept.

SELECT dt.did, dt.dname, dt.chair_ssno
FROM dept as dt
WHERE dt.num_majors = 4 /*user-specific*/

Unclustered hash index on num_majors in Dept.


SELECT dt.did, dt.dname, MIN(dt.budget) 
FROM dept as dt, dept as dt1
WHERE dt.budget = (SELECT MIN(dt1.budget)
				   FROM dept as dt1)
GROUP BY dt.did;

Clustered B+ tree index on budget in Dept.

SELECT *
FROM dept, prof
WHERE dept.chair_ssno = prof.ssno;

 Unclustered B+ tree index on chair_ssno in Dept. And unclustered hash index on ssno in Prof. 
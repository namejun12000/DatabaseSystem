/* 
Homework-4
Name: Nam Jun Lee
Student Number: 11606459
*/

/*Question 1.
Find the distinct courses that ‘SYS’ track students in 'CptS' major are enrolled in. Return 
the courseno and credits for those courses. Return results sorted based on courseno.
*/
SELECT DISTINCT cs.courseno, cs.credits
FROM course cs, student st, enroll er
WHERE st.sid = er.sid 
	AND cs.courseno = er.courseno 
	AND st.trackcode = 'SYS' 
	AND st.major = 'CptS'
ORDER BY courseno;

/*Question 2.
Find the sorted names, ids, majors and track codes of the students who are enrolled in 
more than 18 credits (19 or above). 
*/
SELECT st.sname, st.sid, st.major, st.trackcode, SUM(cs.credits)
FROM student st, course cs, enroll er
WHERE st.sid = er.sid 
	AND cs.courseno = er.courseno 
GROUP BY st.sid
HAVING SUM(cs.credits) > 18
ORDER BY sname, sid, major, trackcode;

/*Question 3.
Find the courses that only 'SE' track students in 'CptS major have been enrolled in. Give 
an answer without using the set EXCEPT operator.
*/
SELECT DISTINCT courseno
FROM student st, enroll er
WHERE er.sid = st.sid 
	AND st.trackcode = 'SE' 
 	AND st.major = 'CptS'
 	AND er.courseno NOT IN (
 	SELECT courseno
 	FROM student st, enroll er
 	WHERE st.sid = er.sid 
		AND st.trackcode <> 'SE')
		AND er.courseno NOT IN (
		SELECT courseno
		FROM student st, enroll er
		WHERE st.sid = er.sid
			AND st.major <> 'CptS');

/*Question 4.
Find the students who have enrolled in the courses that Diane enrolled and earned the 
same grade Diane earned in those courses. Return the student name, sID, major as well 
as the courseno and grade for those courses.
*/
SELECT st.sname, st.sid, st.major, er.courseno, er.grade
FROM student st, student st1, enroll er, enroll er1
WHERE st1.sid = er1.sid 
	AND st.sid = er.sid 
	AND st1.sname = 'Diane' 
	AND er1.courseno = er.courseno 
	AND er1.grade = er.grade 
	AND st1.sid <> st.sid
ORDER BY sname;

/*Question 5.
Find the students in 'CptS' major who are not enrolled in any classes. Return their names
and sIDs. (Note: Give a solution using OUTER JOIN)
*/
SELECT sname, student.sid
FROM student FULL OUTER JOIN enroll
ON student.sid = enroll.sid
WHERE major = 'CptS' 
	AND courseno IS NULL 
ORDER BY sname;

/*Question 6.
Find the courses given in the ‘Sloan’ building which have enrolled more students than 
their enrollment limit. Return the courseno, enroll_limit, and the actual enrollment for 
those courses.
*/
SELECT cs.courseno, cs.enroll_limit, COUNT(er.sid) as enrollnum
FROM course cs, enroll er
WHERE cs.courseno = er.courseno 
	AND cs.classroom LIKE 'Sloan%'
GROUP BY cs.courseno
HAVING COUNT(er.sid) > enroll_limit
ORDER BY enroll_limit;

/*Question 7.
Find 'CptS' major students who enrolled in a course for which there exists a prerequisite 
that the student got a grade lower than “2”. (For example, Alice (sid: 12583589) was 
enrolled in CptS355 but had a grade 1.75 in prerequisite CptS223.) Return the names 
and sIDs of those students and the courseno of the course (i.e., the course whose prereq 
had a low grade).
*/
SELECT st.sname, er.sid, er.courseno
FROM student st, enroll er
WHERE st.sid = er.sid 
	AND st.major = 'CptS' AND
EXISTS
	(SELECT er1.sid, er1.courseno, pr.courseno, pr.precourseno
	FROM enroll er1, prereq pr
	WHERE (er1.courseno = pr.precourseno)
	 	AND (er.courseno = pr.courseno)
		AND (er.sid = er1.sid)
		AND (er1.grade < 2))
ORDER BY courseno;

/*Question 8.
For each ‘CptS’ course, find the percentage of the students who failed the course. 
Assume a passing grade is 2 or above. (Note: Assume students who didn’t earn a grade in 
class should be excluded in average calculation. Also assume all CptS courses start with 
the ‘CptS’ prefix).
*/
SELECT Temp1.courseno, Temp2.passgrade/Temp1.csCpts  as passrate
FROM (
	SELECT courseno, COUNT(courseno) as csCpts
	FROM enroll
	WHERE courseno LIKE 'CptS%'
	GROUP BY courseno) as Temp1,
	(
	SELECT courseno, COUNT(grade) * 100 as passgrade
	FROM enroll
	WHERE courseno LIKE 'CptS%' AND 
	grade >= 2
	GROUP BY courseno) as Temp2
WHERE Temp1.courseno = Temp2.courseno
ORDER BY courseno;

/*Question 9. */
/*(i) explain what the expression is doing:

This relational algebraic expression shows the course no. including two or more pre-required courses
and the number of pre-required courses for each course (equal or more than two) 
using Course and Prereq table. 
*/

/*(ii) write an equivalent SQL query*/
SELECT cr.courseno, COUNT(pr.precourseno) as pCount
FROM course cr, prereq pr
WHERE cr.courseno = pr.courseno
GROUP BY cr.courseno
HAVING COUNT(DISTINCT pr.precourseno) >= 2
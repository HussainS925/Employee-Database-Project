#This file holds the queries for sql.

#Query for the employee overview home page. 
EMPLOYEE_OVERVIEW_UNSORTED = """SELECT * FROM employee_overview """

EMPLOYEE_ORDERBY_FNAME_ASC = """ORDER BY Fname ASC, Minit ASC, Lname ASC """

EMPLOYEE_ORDERBY_FNAME_DESC = """ORDER BY Fname DESC, Minit DESC, Lname DESC """

EMPLOYEE_ORDERBY_LNAME_ASC = """ORDER BY Lname ASC, Fname ASC, Minit ASC """

EMPLOYEE_ORDERBY_LNAME_DESC = """ORDER BY Lname DESC, Fname DESC, Minit DESC """

EMPLOYEE_ORDERBY_HOURS_ASC = """ORDER BY thours ASC NULLS FIRST, Fname ASC, Minit ASC, Lname ASC """

EMPLOYEE_ORDERBY_HOURS_DESC = """ORDER BY thours DESC NULLS LAST, Fname DESC, Minit DESC, Lname DESC """

#Query to get department names
DEPARTMENT_NAME = """SELECT Dname, Dnumber FROM department;"""

# Query for the manager overview home page.
MANAGER_OVERVIEW_UNSORTED =  """SELECT
                        d.Dname,
                        d.Dnumber,
                        COALESCE(
                         m.Fname || ' ' || COALESCE(m.Minit || '. ', '') || m.Lname,
                        'N/A'
                        ) AS manager_name,
                        COUNT(DISTINCT e.Ssn) AS department_employee_count,
                        COALESCE(SUM(w.Hours), 0) AS department_total_hours
                        FROM Department d
                        LEFT JOIN Employee m ON d.Mgr_ssn = m.Ssn
                        LEFT JOIN Employee e ON e.Dno = d.Dnumber
                        LEFT JOIN Works_On w ON w.Essn = e.Ssn
                        GROUP BY d.Dname, d.Dnumber, m.Fname, m.Minit, m.Lname;"""

#Query for projects

PROJECT_OVERVIEW_UNSORTED = """SELECT p.pname, d.dname, 
COUNT(DISTINCT e.ssn) AS employee_count, 
COALESCE(SUM(w.hours), 0) AS total_hours
FROM project p 
LEFT OUTER JOIN department d ON p.dnum = d.dnumber
LEFT OUTER JOIN works_on w ON w.pno = p.pnumber
LEFT OUTER JOIN employee e ON w.essn = e.ssn
GROUP BY p.pname, d.dname """

PROJECT_OVERVIEW_HEADCOUNT_ASC = """ORDER BY employee_count ASC """

PROJECT_OVERVIEW_HEADCOUNT_DESC = """ORDER BY employee_count DESC """

PROJECT_OVERVIEW_HOURS_ASC = """ORDER BY total_hours ASC """

PROJECT_OVERVIEW_HOURS_DESC = """ORDER BY total_hours DESC """

#Upsert query to add / update hours
PROJECT_UPSERT_HOURS = """INSERT INTO Works_On (Essn, Pno, Hours)
                          VALUES (%s, %s, %s)
                          ON CONFLICT (Essn, Pno)
                          DO UPDATE SET Hours = Works_On.Hours + EXCLUDED.Hours;"""

GET_PNO_ON_NAME = """SELECT pnumber FROM project WHERE pname = %s;"""


#Query to get employee names and info for updating employees
EMPLOYEE_NAME = """SELECT fname, minit, lname, ssn, address, salary, Dno FROM EMPLOYEE;"""

#Query to edit employee
EMPLOYEE_EDIT = """UPDATE Employee
                   SET address = %s,
                       Salary = %s,
                       Dno = %s
                   WHERE Ssn = %s;"""

#Query to delete employee
EMPLOYEE_DELETE = """DELETE FROM Employee
                     WHERE Ssn = %s;"""

#Query to insert new employee
EMPLOYEE_INSERT = """INSERT INTO Employee
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
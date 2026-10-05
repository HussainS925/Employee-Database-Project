#This program handles connections to the database.

import psycopg2, queries
from werkzeug.security import check_password_hash

DATABASE_CONFIG = {
    "dbname": "A4",
    "user": "postgres",
    "password": "1286341",
    "host": "localhost",
    "port": "5432"
}

def get_db_connection():
    conn = psycopg2.connect(**DATABASE_CONFIG)
    return conn

#Returns a table of employees for the employee overview page
#sorts and filters the employee overview table. 
#valid sort_by: fname, lname, thours
#valid direction: asc, desc
#Can filter basd on fname, middle initial, last name, department name
def get_employees(sort_by, direction, fname, m_i, lname, dname):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = queries.EMPLOYEE_OVERVIEW_UNSORTED

    order_str = build_sortby(sort_by, direction)

    res = build_where(fname, m_i, lname, dname)

    #If the resulting of build_where is none, then only add sorting to the query.
    #If there exists filters, add the having_str first then order string to query.
    if res is not None:

        arg_arr, where_str = res
        query += where_str + " " + order_str + ";"
        cursor.execute(query, arg_arr)
    
    else:
        query += order_str + ";"
        cursor.execute(query)
    

    employees = cursor.fetchall()
    cursor.close()
    conn.close()
    return employees

# Returns the table of managers for the manager overview page
def get_managers():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(queries.MANAGER_OVERVIEW_UNSORTED)
    managers = cursor.fetchall()

    cursor.close()
    conn.close()
    return managers

# Returns the table of projects for the portfolio summary
def get_projects(sort_by, direction):

    sort_query = ""

    if sort_by == 'hcount':
        if direction == 'desc':
            sort_query = queries.PROJECT_OVERVIEW_HEADCOUNT_DESC
        else:
            sort_query = queries.PROJECT_OVERVIEW_HEADCOUNT_ASC
    
    elif sort_by == 'thours':
        if direction == 'desc':
            sort_query = queries.PROJECT_OVERVIEW_HOURS_DESC
        else:
            sort_query = queries.PROJECT_OVERVIEW_HOURS_ASC
        
    query = queries.PROJECT_OVERVIEW_UNSORTED + sort_query

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(query)
    projects = cursor.fetchall()

    cursor.close()
    conn.close()
    return projects

#Build the ORDER BY clause for employee overview sorting
def build_sortby(sort_by, direction):

    if sort_by == 'fname':
        if direction == 'desc':
            return queries.EMPLOYEE_ORDERBY_FNAME_DESC
        else:
            return queries.EMPLOYEE_ORDERBY_FNAME_ASC
    
    elif sort_by == 'lname':
        if direction == 'desc':
            return queries.EMPLOYEE_ORDERBY_LNAME_DESC
        else:
            return queries.EMPLOYEE_ORDERBY_LNAME_ASC

    elif sort_by == 'thours':
        if direction == 'desc':
            return queries.EMPLOYEE_ORDERBY_HOURS_DESC
        else:
            return queries.EMPLOYEE_ORDERBY_HOURS_ASC
    
    else:
        return ""

#Build the WHERE clause for employee overview filtering
#Returns None if there is no filters, else return the WHERE clause
#and the arguments to WHERE clause for parametrization
def build_where(fname, m_i, lname, dname):

    n_args = 0
    args_arr = []

    clauses = []

    if fname:

        n_args += 1
        args_arr.append("%" + fname.strip() + "%")
        clauses.append("Fname ILIKE %s")

    if m_i:

        n_args += 1
        args_arr.append("%" + m_i.strip() + "%")
        clauses.append("Minit ILIKE %s")

    if lname:

        n_args += 1
        args_arr.append("%" + lname.strip() + "%")
        clauses.append("Lname ILIKE %s")     

    if dname:

        n_args += 1
        args_arr.append(dname)
        clauses.append("Dname LIKE %s")

    query_str = "WHERE " + " AND ".join(clauses)

    if n_args > 0:
        return args_arr, query_str
    else:
        return None



#Gets the names and numbers of the departments 
def get_department_name():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(queries.DEPARTMENT_NAME)
    deps = cursor.fetchall()

    cursor.close()
    conn.close()
    return deps

#Gets the name and ssn of employee
def get_employee_name():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(queries.EMPLOYEE_NAME)
    emps = cursor.fetchall()

    cursor.close()
    conn.close()
    return emps

#Gets a tuple for the employee and inserts it into employee table
def insert_employee(emp_tuple):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(queries.EMPLOYEE_INSERT,emp_tuple)
    conn.commit()

    cursor.close()
    conn.close()

#gets tuple containing address, salary, department number, and ssn
#in that order and edits the table accorind to ssn
def edit_employee(emp_tuple):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(queries.EMPLOYEE_EDIT,emp_tuple)
    conn.commit()

    cursor.close()
    conn.close()

#Deletes an employee based on ssn,
def del_employee(ssn):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(queries.EMPLOYEE_DELETE,(ssn,))
    conn.commit()

    cursor.close()
    conn.close()


# this function ensures that the user inputted a correct username and password
def validate_user(user, password):

    try:
        conn = get_db_connection()
        cursor = conn.cursor() 

        cursor.execute("SELECT password_hash, role FROM app_user WHERE username = %s ;", (user, ))

        users = cursor.fetchall()

        conn.commit()
        cursor.close()
        conn.close()

        if (len(users) == 0):
            print("invalid username")
            return None

        else:

            for tuple in users:

                if (check_password_hash(tuple[0], password)):
                    print("match")
                    return (tuple[1])

                else:
                    print("incorrect password!")
                    return None

    except Exception as e:
        print("%s", e)
        return None

def get_all_employees():
    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """
        SELECT e.ssn, e.fname, e.minit, e.lname
        FROM Employee e
        ORDER BY e.lname, e.fname;
    """

    cursor.execute(sql)
    employees = cursor.fetchall()

    cursor.close()
    conn.close()
    return employees

def get_project_details(pname):

    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """
        SELECT e.fname, e.minit, e.lname, COALESCE(w.hours, 0)
        FROM Project p
        JOIN Works_On w ON w.pno = p.pnumber
        JOIN Employee e ON e.ssn = w.essn
        WHERE p.pname = %s
        ORDER BY e.lname, e.fname;
    """

    cursor.execute(sql, (pname,))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()
    return rows


def upsert_works_on(essn, pno, hours):
    conn = get_db_connection()
    cursor = conn.cursor()

    sql = queries.PROJECT_UPSERT_HOURS

    cursor.execute(sql, (essn, pno, hours))
    conn.commit()

    cursor.close()
    conn.close()

#Gets the project number when project name is given
def get_pno(pname):
    conn = get_db_connection()
    cursor = conn.cursor()

    sql = queries.GET_PNO_ON_NAME
    pname = pname.strip()    

    cursor.execute(sql, (pname,))
    res = cursor.fetchone()
    
    if res:
        res = res[0]

    cursor.close()
    conn.close()

    return res

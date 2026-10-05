from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, session
from db_manager import *
from add_user import *
from extra import *
import numpy as np
import pandas as pd

# Flask will look for templates in the "HTML" folder (same level as app.py)
app = Flask(__name__, template_folder="HTML")

# TODO: replace this with a more secure random key later
app.secret_key = "dev-key-change-later"

USER_LIST = [["user1","user","viewer"],
             ["admin1","admin","admin"]]

add_to_app_user(USER_LIST)


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if "username" not in session:
            return redirect(url_for("login"))
        return view(**kwargs)
    return wrapped_view


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        # TEMP: accept any anything username/password.
        if username and password:

            role = validate_user(username, password)

            if role is not None:
                session["username"] = username
                session["role"] = role
                return redirect(url_for("home"))

            # session["username"] = username

            # print(username)
            # print(password)

            else:
                return render_template("login.html", error="Invalid Login Details")

            
        else:
            # should prolly add an error
            return render_template("login.html")

    # GET
    return render_template("login.html")


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))

#Home page, employee overview.
@app.route("/home", methods=["GET", "POST"])
@login_required
def home():

    deps = get_department_name()

    sort_by = request.args.get('sort_by', None)
    direction = request.args.get('direction','asc')
    fname = request.args.get('fname',"")
    m_i = request.args.get('m_i',"")
    lname = request.args.get('lname',"")
    dname = request.args.get('dname',"")
    
    #display arrows for sorting
    arrows = {
        'fname': '▲▼',
        'lname': '▲▼',
        'thours': '▲▼'
    }

    next_direction= {
        'fname': 'asc',
        'lname': 'asc',
        'thours': 'asc'
    }

    employees = get_employees(sort_by, direction, fname, m_i, lname, dname)

    if sort_by is not None:
        arrows[sort_by] = '▲' if direction == 'asc' else '▼'
        next_direction[sort_by] = 'desc' if direction == 'asc' else 'asc'


    return render_template(
        "Home.html",          
        username=session.get("username"),
        employees=employees,
        arrows=arrows,
        next_direction=next_direction,
        deps=deps
    )

#Projects page, portfolio summary
@app.route("/projects")
@login_required
def projects():

    sort_by = request.args.get('sort_by', None)
    direction = request.args.get('direction','asc')

    arrows = {
        'hcount': '▲▼',
        'thours': '▲▼'
    }

    next_direction= {
        'hcount': 'asc',
        'thours': 'asc'
    }
    
    project_list = get_projects(sort_by, direction)

    if sort_by is not None:
        arrows[sort_by] = '▲' if direction == 'asc' else '▼'
        next_direction[sort_by] = 'desc' if direction == 'asc' else 'asc'

    return render_template(
        "Projects.html",          
        username=session.get("username"),
        project_list=project_list,
        arrows=arrows,
        next_direction=next_direction
    )

@app.route("/details", methods=["GET", "POST"])
@login_required
def proj_details():

    proj_name = request.args.get('pname')

    if session.get("role") == "admin":
        employees_all = get_all_employees()  
        template = "Proj_Details_Admin.html"

        if request.method == "POST":

            ssn = request.form.get("essn")
            pno = get_pno(proj_name)
            hours = request.form.get("hours")

            upsert_works_on(ssn, pno, hours)

    else:
        employees_all = None
        template = "Proj_Details.html"
    
    proj_employees = []
    proj_employees = get_project_details(proj_name)

    # Finding average hours for the project using NUMPY

    hours = np.array([row[3] for row in proj_employees])
    avg_hours = np.mean(hours)

    # Creating dataframe with Pandas to display percentage of hours worked by each employee on the project

    df = pd.DataFrame(proj_employees, columns=["First Name", "Middle Initial", "Last Name", "Hours"])

    # Ensuring that the "Hours" column is numeric for calculations

    df["Hours"] = pd.to_numeric(df["Hours"])

    total_hours = df["Hours"].sum()

    if total_hours > 0:

        df["Percentage"] = (df["Hours"] / total_hours * 100).round(2)
        
    else:

        df["Percentage"] = 0

    # Convert back to list to display on frontend
    proj_employees = df.values.tolist()

    return render_template(
        template,          
        username=session.get("username"),
        proj_employees=proj_employees,
        project_name=proj_name,
        employees_all=employees_all,
        avg_hours=avg_hours
    )

@app.route("/managers")
@login_required
def managers():
    managers = get_managers()

    return render_template(
        "Managers.html",          
        username=session.get("username"),
        managers=managers
    )

#inserts, edits, deletes employees. If user is not an admin, the restricted pages shows instead
#of Employee mangement page. 
@app.route("/emp_manage", methods=["GET", "POST"])
@login_required
def emp_management():

    if session.get("role") == "admin":

        employee_names = get_employee_name()
        deps = get_department_name()
        success_msg = ""

        if request.method == "POST":
            action = request.form.get("type")

            if action == "add":
            
                try:

                    super_ssn = request.form.get("sup_ssn").strip()

                    if (super_ssn == ""):
                        super_ssn = None
                    

                    emp_tuple = (
                        request.form.get("fname").strip(),
                        request.form.get("m_i").strip(),
                        request.form.get("lname").strip(),
                        request.form.get("ssn"),
                        request.form.get("address").strip(),
                        request.form.get("sex"),
                        request.form.get("salary").strip(),
                        super_ssn,
                        request.form.get("dname"),
                        request.form.get("bdate"),
                        request.form.get("empdate"),
                    )

                    insert_employee(emp_tuple)      
                    success_msg = "Employee added successfully!"       

                except Exception as e:
                    success_msg = e
                    print(e)

            elif action == "update":

                try:

                    emp_ssn = request.form.get("employee")
                    address = request.form.get("edit_add").strip()
                    salary = request.form.get("edit_salary").strip()
                    dno = request.form.get("edit_dep")

                    emp_tuple = (address, salary, dno, emp_ssn)

                    edit_employee(emp_tuple)
                    success_msg = "Employee edited successfully!" 

                except Exception as e:
                    success_msg = e
                    print(e)
                    
            elif action == "delete":
                try:

                    emp_ssn = request.form.get("del_employee")

                    del_employee(emp_ssn)
                    success_msg = "Employee deleted successfully!" 

                except Exception as e:
                    success_msg = """Cannot delete employee: They are still assigned to projects, have dependents listed,
                                        or are a manager/supervisor."""
                    print(e)

        return render_template(
            "Emp_Manage_Admin.html",          
            username=session.get("username"),
            employees=employee_names,
            deps=deps,
            Success_message=success_msg
        )
    else:

        return render_template(
            "Restricted.html",          
            username=session.get("username"),
        )



@app.route("/")
def index():
    # Redirect root URL to /login
    return redirect(url_for("login"))


@app.route("/home/export_csv")
@login_required
def home_export_csv():
    # Use the same query params as /home so it exports the
    # currently filtered and sorted employee list.
    sort_by = request.args.get('sort_by', None)
    direction = request.args.get('direction', 'asc')
    fname = request.args.get('fname', "")
    m_i = request.args.get('m_i', "")
    lname = request.args.get('lname', "")
    dname = request.args.get('dname', "")

    return export_employees_csv(sort_by, direction, fname, m_i, lname, dname)



if __name__ == "__main__":
    app.run(debug=True)

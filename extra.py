import csv
import io

from flask import Response
from openpyxl import load_workbook

from db_manager import get_employees, get_db_connection


def export_employees_csv(sort_by, direction, fname, m_i, lname, dname) -> Response:
    """
    Build a CSV HTTP response for the current employee overview
    using the same filters and sorting as the /home page.
    """
    employees = get_employees(sort_by, direction, fname, m_i, lname, dname)

    output = io.StringIO()
    writer = csv.writer(output)

    # Header row matches Home.html columns
    writer.writerow(
        [
            "Fname",
            "Minit",
            "Lname",
            "Department",
            "Dependents",
            "Projects",
            "TotalHours",
        ]
    )

    for row in employees:
        writer.writerow(row)

    output.seek(0)

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": 'attachment; filename="employees.csv"'},
    )

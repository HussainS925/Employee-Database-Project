# README

## 1. Setup environment 
Setup the python virtual environment on your machine. 

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2. Load schema into your database

1. Create  a new database if you haven't already
    example if you are in your psql: `CREATE DATABASE mydatabase;`

2. Connect to your database
    example if you are in your psql: `\c mydatabase`

3. Run the sql files `company_v3.02.sql` and `team_setup.sql` in your database example if you are in your psql:  
    `\i fileapath/company_v3.02.sql`  
    `\i fileapath/team_setup.sql`


## 3. Setup database configuration in db_manager.py and app.py
Find the following code in `db_manager.py` and `app.py`

```python
DATABASE_CONFIG = {
    "dbname": "A4",
    "user": "postgres",
    "password": "1286341",
    "host": "localhost",
    "port": "5432"
}
```

replace `A4` with your database's name, `postgres` with your database's username, and `1286341` with your database's password.

## 4. Run the app
Make sure you are in your `app.py` directory and then run `python3 app.py`

## 5. Login Details
These logins are automatically made when you run app.py. You can add or modify by going to `add_user.py` and adding more users to `USER_LIST` before running the app.

    For the administrator role:
    Username: admin1
    Password: admin

    For the viewer role:
    Username: user1
    Password: user

## 6. Indexes
These indexes were created for our schema:

1. Creates an index for the column `fname` on the table `Employee`. Speeds up sorting with first name on employee overview page.

```sql 
    CREATE INDEX idx_fname ON Employee (fname);
```

2. Creates an index for the column `lname` on the table `Employee`. Speeds up sorting with last name on employee overview page.

```sql
    CREATE INDEX idx_fname ON Employee (lname);
```

3. Creates an index of ssn for the column `ssn` on the `Employee` table. Speeds up searching on ssn while updating or deleting employees in the employee management page. And speeds up searching when adding hours to employees in the project details page.

```sql
    CREATE INDEX idx_ssn ON Employee (ssn);
```
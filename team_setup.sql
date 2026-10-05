DROP VIEW IF EXISTS Employee_overview;
DROP TABLE IF EXISTS app_user;

CREATE TABLE app_user (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('admin','viewer'))
);

CREATE OR REPLACE VIEW Employee_overview AS
SELECT Fname, Minit, Lname, Dname, COALESCE(d.d_count,0) AS Ndep, COALESCE(w.c_pno,0) AS Nproj, COALESCE(w.s_hours,0) AS Thours
FROM employee e LEFT JOIN department ON Dno = Dnumber 
LEFT JOIN (
    SELECT essn, Count(dep.dependent_name) AS d_count
    FROM dependent dep
    GROUP BY essn
) AS d ON e.ssn = d.essn
LEFT JOIN (
    SELECT essn, COUNT(Pno) AS c_pno, SUM(hours) AS s_hours
    FROM works_on 
    GROUP BY essn
) AS w ON e.ssn = w.essn;

CREATE INDEX idx_fname ON Employee (fname);

CREATE INDEX idx_fname ON Employee (lname);

CREATE INDEX idx_ssn ON Employee (ssn);

from flask import Flask, jsonify
#https://www.youtube.com/watch?v=8ebIEefhBpM
from werkzeug.security import generate_password_hash
import psycopg2

app = Flask(__name__)


DATABASE_CONFIG = {
    "dbname": "A4",
    "user": "postgres",
    "password": "1286341",
    "host": "localhost",
    "port": "5432"
}

#List of users to enter into database. format: [username,password,role]
#Roles are viewer and admin
USER_LIST = [["user1","user","viewer"],
             ["admin1","admin","admin"]]


def get_db_connection():
    conn = psycopg2.connect(**DATABASE_CONFIG)
    return conn


# this function creates a new user with a new username and password that is hashed, and also assigns the new user a role
def add_to_app_user(user_list):


    try:
        conn = get_db_connection()
        cursor = conn.cursor() 

        for user in user_list:
            #this is a test insert querry but we can make the username, password_hash, and role thing a user generated later
            cursor.execute("INSERT INTO app_user (username, password_hash, role) VALUES (%s, %s, %s)", 
                        (user[0], generate_password_hash(user[1]), user[2]))

        conn.commit()
        cursor.close()
        conn.close()

    except Exception as e:
        print("%s", e)



if __name__ == "__main__":
   add_to_app_user(USER_LIST)



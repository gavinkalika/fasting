from flask import Flask
from datetime import datetime, timezone
import mysql.connector
from mysql.connector import Error
import yaml

app = Flask(__name__)


@app.route('/')
def run():
    return 'Hello, World!'


# @app.route('/start-fast')
# def start_fast():
#     start_fast_time = datetime.now(timezone.utc)
#
#     with open(r'../.../config/db.yaml') as file:
#         db_config = yaml.load(file, Loader=yaml.FullLoader)
#
#     #     save fast
#     mydb = mysql.connector.connect(
#         host=db_config['host'],
#         user=db_config['user'],
#         password=db_config['password'],
#         database="fasting"
#     )
#     mycursor = mydb.cursor()
#
#     sql = "INSERT INTO fast (created_time, end_time) VALUES (%s, %s)"
#     val = (start_fast_time, "NULL")
#     mycursor.execute(sql, val)
#
#     mydb.commit()
#  return 200 or throw error

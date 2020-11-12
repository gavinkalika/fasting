from datetime import datetime, timezone
import mysql.connector

import yaml


class FastLoader:

    def __init__(self):
        with open('../config/db.yaml') as file:
            db_config = yaml.load(file, Loader=yaml.FullLoader)

        self.db_conn = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database="fasting"
        )

    def load_all(self):
        db_cursor = self.db_conn.cursor()

        sql = "SELECT created_time, end_time FROM fast"
        db_cursor.execute(sql)

        return db_cursor.fetchall()

    def __repr__(self):
        return 'Fast Loader'

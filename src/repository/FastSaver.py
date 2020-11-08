from datetime import datetime, timezone
import mysql.connector

import yaml


class FastSaver:

    def __init__(self):
        with open('../config/db.yaml') as file:
            db_config = yaml.load(file, Loader=yaml.FullLoader)

        self.db_conn = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database="fasting"
        )

    def start_fast(self):
        start_fast_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

        db_cursor = self.db_conn.cursor()

        sql = "INSERT INTO fast (created_time) VALUES ('{0}')".format(start_fast_time)
        db_cursor.execute(sql)

        self.db_conn.commit()

    def end_fast(self):
        pass

    def __repr__(self):
        return 'Fast Saver'

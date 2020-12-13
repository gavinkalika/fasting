from datetime import datetime, timezone
from mysql.connector import MySQLConnection


class UserLoader:

    def __init__(self, db_conn: MySQLConnection):
        self.db_conn = db_conn

    def load_user_by_email(self, email: str) -> tuple:
        db_cursor = self.db_conn.cursor()

        sql = "SELECT email from user WHERE email = '{0}'".format(email)

        db_cursor.execute(sql)

        result = db_cursor.fetchone()

        if result is None:
            raise Exception("User does not exist.")

        return result

    def __repr__(self):
        return 'User Saver'

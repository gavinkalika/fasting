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

        if len(result) > 1:
            raise Exception("Too many users with this e-mail address.")

        return result

    def load_user_id_by_email(self, email: str) -> tuple:
        db_cursor = self.db_conn.cursor()

        sql = "SELECT id from user WHERE email = '{0}'".format(email)

        db_cursor.execute(sql)

        result = db_cursor.fetchone()

        if result is None:
            raise Exception("User does not exist.")

        if len(result) > 1:
            raise Exception("Too many users with this e-mail address.")

        return result[0]

    def __repr__(self):
        return 'User Saver'

from datetime import datetime, timezone
from mysql.connector import MySQLConnection


class UserSaver:

    def __init__(self, db_conn: MySQLConnection):
        """[summary]

        Args:
            db_conn ([type]): [description]
        """
        self.db_conn = db_conn

    def save_user(self, email: str, password: str) -> None:
        db_cursor = self.db_conn.cursor()

        sql = "INSERT INTO user (email, password) VALUES ('{0}', '{1}')".format(email, password)

        db_cursor.execute(sql)

        self.db_conn.commit()

    def __repr__(self):
        return 'User Saver'

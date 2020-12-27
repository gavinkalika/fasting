from mysql.connector import MySQLConnection

from app.repository.UserLoader import UserLoader


class FastLoader:

    def __init__(self, db_conn: MySQLConnection, user_loader: UserLoader):
        """Constructor to get list of fasts."""
        self.user_loader = user_loader
        self.db_conn = db_conn

    def load_all(self, email: str) -> tuple:
        """Use this method to load all fasts

        Returns:
        array: List of fasts
        """

        db_cursor = self.db_conn.cursor()

        self.user_loader.load_user_by_email(email)

        sql = "SELECT created_time, end_time FROM fast"
        db_cursor.execute(sql)

        return db_cursor.fetchall()

    def load_all_that_have_no_end_time(self, email: str) -> tuple:
        """Use this method to load all fasts

        Returns:
        array: List of fasts
        """

        db_cursor = self.db_conn.cursor()

        user_id = self.user_loader.load_user_id_by_email(email)

        sql = "SELECT created_time, end_time, user_id, id  FROM fast WHERE end_time is null AND user_id = {0}".format(user_id)
        db_cursor.execute(sql)

        return db_cursor.fetchall()

    def __repr__(self):
        return 'Fast Loader'

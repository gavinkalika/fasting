from datetime import datetime, timezone

from mysql.connector import MySQLConnection

from app.exception.ExceedLimitException import ExceedLimitException
from app.repository.FastLoader import FastLoader
from app.repository.UserLoader import UserLoader


class FastSaver:

    def __init__(self, db_conn: MySQLConnection, user_loader: UserLoader, fast_loader: FastLoader):
        """Constructor to get list of fasts."""
        self.fast_loader = fast_loader
        self.user_loader = user_loader
        self.db_conn = db_conn

    def start_fast(self, email) -> None:
        """Use this method to start a fast timer"""
        user_id = self.user_loader.load_user_id_by_email(email)

        active_fasts = self.fast_loader.load_all_that_have_no_end_time(email)

        if len(active_fasts) >= 1:
            raise ExceedLimitException('This user, {0}, already has an active fast open'.format(email))

        start_fast_time = self.__get_time()

        db_cursor = self.db_conn.cursor()

        sql = "INSERT INTO fast (created_time, user_id) VALUES ('{0}', '{1}')".format(start_fast_time, user_id)
        db_cursor.execute(sql)

        self.db_conn.commit()

    def end_fast(self, email) -> None:
        """Use this method to end fasts"""
        user_id = self.user_loader.load_user_id_by_email(email)
        active_fasts = self.fast_loader.load_all_that_have_no_end_time(email)
        active_fast = active_fasts[0]['id']

        end_fast_time = self.__get_time()

        db_cursor = self.db_conn.cursor()

        sql = "UPDATE fast " \
              "SET end_time = '{0}'" \
              "WHERE id = {1}".format(end_fast_time, active_fast)
        db_cursor.execute(sql)

        self.db_conn.commit()

    def __get_time(self) -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    def __repr__(self):
        return 'Fast Saver'

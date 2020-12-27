from datetime import datetime, timezone
from mysql.connector import MySQLConnection

from app.enum.UserSettingEnum import UserSettingEnum


class UserSaver:

    def __init__(self, db_conn: MySQLConnection):
        """[summary]

        Args:
            db_conn ([type]): [description]
        """
        self.db_conn = db_conn

    def save_user(self, email: str, password: str) -> None:
        db_cursor = self.db_conn.cursor()

        sql_user = "INSERT INTO user (email, password) VALUES ('{0}', '{1}')".format(email, password)

        db_cursor.execute(sql_user)

        user_id = db_cursor.get_cursor()

        default_timezone = UserSettingEnum.get_default_value('timezone')
        setting_id = UserSettingEnum.get_setting_id_by_label('timezone')
        sql_user_setting = "INSERT INTO fasting.user_setting (user_id, user_setting_id, value) VALUES ('{0}', '{1}', " \
                           "'{2}')".format(user_id, setting_id, default_timezone)

        db_cursor.execute(sql_user_setting)

        self.db_conn.commit()

    def __repr__(self):
        return 'User Saver'

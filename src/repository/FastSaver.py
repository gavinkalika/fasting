from datetime import datetime, timezone


class FastSaver:

    def __init__(self, db_conn):
        """Constructor to get list of fasts."""
        self.db_conn = db_conn

    def start_fast(self):
        """Use this method to start a fast timer"""

        start_fast_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

        db_cursor = self.db_conn.cursor()

        sql = "INSERT INTO fast (created_time) VALUES ('{0}')".format(start_fast_time)
        db_cursor.execute(sql)

        self.db_conn.commit()

    def end_fast(self):
        """Use this method to end fasts"""

        end_fast_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

        db_cursor = self.db_conn.cursor()

        sql = "UPDATE fast " \
              "SET end_time = '{0}'" \
              "WHERE end_time IS NULL".format(end_fast_time)
        db_cursor.execute(sql)

        self.db_conn.commit()

    def __repr__(self):
        return 'Fast Saver'

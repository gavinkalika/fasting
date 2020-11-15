class FastLoader:

    def __init__(self, db_conn):
        """Constructor to get list of fasts."""
        self.db_conn = db_conn

    def load_all(self):
        """Use this method to load all fasts

        Returns:
        array: List of fasts
        """

        db_cursor = self.db_conn.cursor()

        sql = "SELECT created_time, end_time FROM fast"
        db_cursor.execute(sql)

        return db_cursor.fetchall()

    def __repr__(self):
        return 'Fast Loader'

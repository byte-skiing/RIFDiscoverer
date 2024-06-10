import os
import sqlite3

class DatabaseConnection: 
    def __init__(self, database_file):
        self.connection_string = database_file
        self._should_run_seed = False
        self._build_schema()
        self._run_seed()

    def connect(self):
        if not os.path.exists(self.connection_string):
            self._should_run_seed = True

        return sqlite3.connect(self.connection_string)

    def get_cursor(self):
        connection = self.connect()
        return connection.cursor()

    def execute(self, query, input_data = None):
        connection = self.connect()
        cursor = connection.cursor()

        if input_data is None:
            cursor.execute(query)
        else:
            cursor.execute(query, input_data)

        result_data = cursor.fetchall()
        connection.commit()
        connection.close()

        if len(result_data) == 1:
            return result_data[0]

        return result_data

    def execute_file(self, file_path):
        connection = self.connect()
        cursor = connection.cursor()

        with open(file_path, 'r') as file:
            cursor.executescript(file.read())

        connection.commit()
        connection.close()

    def _build_schema(self):
        self.execute_file('db/schema.sql')

    def _run_seed(self):
        if not self._should_run_seed:
            return

        self.execute_file('db/seed.sql')

db = DatabaseConnection('db/app.db')

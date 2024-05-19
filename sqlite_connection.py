import os
import sqlite3


class SQLiteConnection:
    """
    A class to manage SQLite database connections and operations.
    """

    def __init__(self, db_name: str):
        """
        Initialize SQLiteConnection object with the specified database name.

        Parameters:
            db_name (str): The name of the SQLite database file.
        """
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def connect(self):
        """
        Connect to the SQLite database.

        Returns:
            int: 0 if connected successfully, otherwise -1.
        """
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            return 0  # OK
        except sqlite3.Error as connect_error:
            print(f"Error connecting to database: '{connect_error}'")
            return -1  # Error

    def create_table(self, table_name: str, columns: dict) -> int:
        """
        Create a table in the SQLite database with the specified name and columns.

        Parameters:
            table_name (str): The name of the table to be created.
            columns (dict): A dictionary defining the columns of the table. 
                            Keys are column names, values are lists where the first element is the data type and subsequent elements are constraints or modifiers.

        Returns:
            int: 0 if table created successfully, otherwise -1.
        """
        try:
            columns_str = ', '.join(
                [f"{column} {column_type}" for column, column_type in columns.items()])
            create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})"
            self.cursor.execute(create_table_query)
            self.connection.commit()
            return 0  # OK
        except sqlite3.Error as create_table_error:
            print(f"Error creating table '{create_table_error}'")
            return -1  # Error

    def insert(self, table_name: str, data: dict) -> int:
        """
        Insert data into the specified table.

        Parameters:
            table_name (str): The name of the table to insert data into.
            data (dict): A dictionary containing column names and their corresponding values.

        Returns:
            int: 0 if data inserted successfully, otherwise -1.
        """
        try:
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['?' for _ in data.keys()])
            insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            self.cursor.execute(insert_query, list(data.values()))
            self.connection.commit()
            return 0  # OK
        except sqlite3.Error as insert_error:
            print(f"Error inserting data '{insert_error}'")
            return -1  # Error

    def execute_sql(self, sql_path=None, sql_query=None):
        """
        Execute SQL queries from a file or a string.

        Parameters:
            sql_path (str, optional): The file path containing the SQL query to execute.
            sql_query (str, optional): The SQL query to execute as a string.

        Returns:
            int: 0 if SQL executed successfully, otherwise -1.
        """
        if (sql_path is None and sql_query is None) or (sql_path is not None and sql_query is not None):
            print("Error: Please provide either a SQL file path or a SQL query string, "
                  "but not both.")
            return -1

        try:
            if sql_path is not None:
                if os.path.exists(sql_path):
                    with open(sql_path, 'r') as file:
                        sql_query = file.read()
                else:
                    print("Error: SQL file not found.")
                    return -1

            self.cursor.executescript(sql_query)
            self.connection.commit()
            return 0  # OK
        except sqlite3.Error as execute_sql_error:
            print(f"Error executing SQL: {execute_sql_error}")
            return -1  # Error

    def select(self, sql_query: str) -> list:
        """
        Execute a SQL query and retrieve the results as a list of tuples.

        Parameters:
            sql_query (str): The SQL query to execute.

        Returns:
            list: A list of tuples containing the results of the query.
        """
        try:
            self.cursor.execute(sql_query)
            results = self.cursor.fetchall()
            return results
        except sqlite3.Error as select_error:
            print(f"Error executing SQL: {select_error}")
            return None

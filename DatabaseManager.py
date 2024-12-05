from typing import List
# import mariadb
# import sys
import mysql.connector
from ConfigManager import ConfigManager


class DatabaseManager:

    def __init__(self):
        # data retrieve queries
        self.get_dbs_query = 'SHOW DATABASES'
        self.get_tables_query = "SHOW TABLES"
        self.get_fields_query = "SHOW FIELDS FROM %t"
        self.get_records_query = "SELECT ? FROM ?"

        # data insertion queries
        self.records_insert_query = "INSERT INTO ? (?) VALUES(?)"
        self.table_creation_query = """CREATE TABLE ? ()"""  # https://www.w3schools.com/sql/sql_foreignkey.asp
        self.database_creation_query = "CREATE DATABASE ?"

        self.config_manager = ConfigManager()
        self.connection = mysql.connector.connect(
            host=self.config_manager.host,
            user=self.config_manager.user,
            password=self.config_manager.password,
            database=self.config_manager.database
        )

    def getAll(self, fields: List[str], table: str):
        pass

    def Get(self, query: str, *args) -> list:
        pass


# try:
#     # connection parameters
#     conn_params = {
#         'user': "harley",
#         'password': "KTJ7UCS74mv]hh[I",
#         'host': "127.0.0.1",
#         'port': 3306,
#         'database': "phishing_emails"
#     }
#
#     # establish a connection
#     connection = mariadb.connect(**conn_params)
#     cursor = connection.cursor()
#
# except mariadb.Error as e:
#     print(f"Error connecting to MariaDB Platform: {e}")
#     sys.exit(1)
#
# print(cursor)


# py -3.11 -m pip install mysql-connector-python
# https://realpython.com/python-mysql/

#bts@siec.education.fr
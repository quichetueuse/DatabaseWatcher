from typing import List
import mariadb
import sys
# import mysql.connector
from ConfigManager import ConfigManager


class DatabaseManager:

    def __init__(self):
        # data retrieve queries
        self._get_dbs_query = 'SHOW DATABASES'
        self._get_tables_query = "SHOW TABLES"
        self._get_fields_query = "SHOW FIELDS FROM %t"
        self._get_records_query = "SELECT ? FROM ?"

        # data insertion queries
        self._records_insert_query = "INSERT INTO ? (?) VALUES(?)"
        self._table_creation_query = """CREATE TABLE ? ()"""  # https://www.w3schools.com/sql/sql_foreignkey.asp
        self._database_creation_query = "CREATE DATABASE ?"

        self._config_manager = ConfigManager()
        # self._connection = mariadb.connect(
        #     host=self._config_manager.host,
        #     user=self._config_manager.user,
        #     password=self._config_manager.password,
        #     database=self._config_manager.database
        # )
        self._connection = mariadb.connect(
            host=self._config_manager.host,
            user=self._config_manager.user,
            password=self._config_manager.password,
            database=self._config_manager.database
        )
        self._cursor = None
        # self._connection.close()

    # def getAll(self, fields: List[str], table: str):
    #     pass

    # def Get(self, query: str, *args) -> list:
    #     self._connection.reconnect()
    #
    #     self._cursor = self._connection.cursor()
    #
    #     print(args)
    #
    #     self._connection.close()
    #     self._cursor = None
    #     return []

    def _getAllTables(self) -> List[tuple]:
        print(self._connection.open)
        self._connection.reconnect()
        self._cursor = self._connection.cursor()

        self._cursor.execute(self._get_tables_query)
        tables = self._cursor.fetchall()

        self._connection.close()
        self._cursor = None
        return tables

    def _getFieldsFromTable(self, table: str) -> List[tuple]:
        self._connection.reconnect()
        self._cursor = self._connection.cursor()

        self._cursor.execute(self._get_fields_query, table)
        fields = self._cursor.fetchall()

        self._connection.close()
        self._cursor = None

        return fields

    def _getRecordsFromTable(self, fields: list, table: str) -> List[tuple]:
        self._connection.reconnect()
        self._cursor = self._connection.cursor()

        self._cursor.execute(self._get_fields_query, (fields, table))
        records = self._cursor.fetchall()

        self._connection.close()
        self._cursor = None

        return records


#
# class DatabaseManager:
#
#     def __init__(self):
#         # data retrieve queries
#         self._get_dbs_query = 'SHOW DATABASES'
#         self._get_tables_query = "SHOW TABLES"
#         self._get_fields_query = "SHOW FIELDS FROM %t"
#         self._get_records_query = "SELECT ? FROM ?"
#
#         # data insertion queries
#         self._records_insert_query = "INSERT INTO ? (?) VALUES(?)"
#         self._table_creation_query = """CREATE TABLE ? ()"""  # https://www.w3schools.com/sql/sql_foreignkey.asp
#         self._database_creation_query = "CREATE DATABASE ?"
#
#         self._config_manager = ConfigManager()
#         self._connection = mysql.connector.connect(
#             host=self._config_manager.host,
#             user=self._config_manager.user,
#             password=self._config_manager.password,
#             database=self._config_manager.database
#         )
#         self._cursor = None
#         self._connection.close()
#
#     def getAll(self, fields: List[str], table: str):
#         pass
#
#     def Get(self, query: str, *args) -> list:
#         self._connection.reconnect()
#
#         self._cursor = self._connection.cursor()
#
#         print(args)
#
#         self._connection.close()
#         self._cursor = None
#         return []
#
#     def _getAllTables(self) -> List[tuple]:
#         self._connection.reconnect()
#         self._cursor = self._connection.cursor()
#
#         self._cursor.execute(self._get_tables_query)
#         tables = self._cursor.fetchall()
#
#         self._connection.close()
#         self._cursor = None
#         return tables
#
#     def _getFieldsFromTable(self, table: str) -> List[tuple]:
#         self._connection.reconnect()
#         self._cursor = self._connection.cursor()
#
#         self._cursor.execute(self._get_fields_query, table)
#         fields = self._cursor.fetchall()
#
#         self._connection.close()
#         self._cursor = None
#
#         return fields
#
#     def _getRecordsFromTable(self, fields: list, table: str) -> List[tuple]:
#         self._connection.reconnect()
#         self._cursor = self._connection.cursor()
#
#         self._cursor.execute(self._get_fields_query, (fields, table))
#         records = self._cursor.fetchall()
#
#         self._connection.close()
#         self._cursor = None
#
#         return records




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







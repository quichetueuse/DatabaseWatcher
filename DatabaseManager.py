from typing import List
import mariadb
import sys

from mariadb import Connection

# import mysql.connector
from ConfigManager import ConfigManager
import colorama

class DatabaseManager:

    def __init__(self, config_manager: ConfigManager):
        # data retrieve queries
        self._get_dbs_query = 'SHOW DATABASES;'
        self._get_tables_query = "SHOW TABLES;"
        self._get_fields_query = "SHOW FIELDS FROM %table;"
        self._get_records_query = "SELECT * FROM %table LIMIT 15;"

        # data insertion queries
        self._records_insert_query = "INSERT INTO %table (%fields) VALUES (?)"
        self._record_update_query_start = "UPDATE %table SET"
        self._record_update_query_end = " WHERE %field=%value"
        self._table_creation_query = "CREATE TABLE %table %fields "  # https://www.w3schools.com/sql/sql_foreignkey.asp
        self._database_creation_query = "CREATE DATABASE ?;"
        self._table_drop_query = "DROP TABLE IF EXISTS %table"
        self._check_record_query = "SELECT COUNT(%field) FROM %table WHERE %field=?"

        self.error_count = 0
        self._config_manager = config_manager
        # self._connection = mariadb.connect(
        #     host=self._config_manager.host,
        #     user=self._config_manager.user,
        #     password=self._config_manager.password,
        #     database=self._config_manager.database
        # )
        self._connection = None
        self._cursor = None
        # self._connection.close()

    def _connectToDBServer(self) -> Connection:
        return mariadb.connect(
            host=self._config_manager.host,
            user=self._config_manager.user,
            password=self._config_manager.password,
            database=self._config_manager.database
        )

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
        # print(self._connection.open)
        # self._connection.reconnect()
        self._connection = self._connectToDBServer()
        self._cursor = self._connection.cursor()

        self._cursor.execute(self._get_tables_query)
        tables = self._cursor.fetchall()

        self._connection.close()
        self._cursor = None
        return tables

    def _getFieldsFromTable(self, table: str) -> List[tuple]:
        self._connection = self._connectToDBServer()
        self._cursor = self._connection.cursor()

        # test = self._get_fields_query.replace('?', table)
        # self._cursor.execute(self._get_fields_query, table)
        self._cursor.execute(self._get_fields_query.replace('%table', table))
        # self._cursor.execute("SELECT * FROM clients WHERE nom= %s", ('Smith',))
        fields = self._cursor.fetchall()

        self._connection.close()
        self._cursor = None

        return fields

    def _getRecordsFromTable(self, table: str) -> List[tuple]:
        self._connection = self._connectToDBServer()
        self._cursor = self._connection.cursor(prepared=True)

        self._cursor.execute(self._get_records_query.replace('%table', table))
        records = self._cursor.fetchall()

        self._connection.close()
        self._cursor = None

        return records

    # def checkIfRecordExists(self, table: str, field: str, record_id: int or str) -> bool:
    #     self._connection = self._connectToDBServer()
    #     self._cursor = self._connection.cursor(prepared=True)
    #     # self._cursor.statement
    #     self._cursor.execute(self._check_record_query.replace('%table', table).replace('%field', field), (record_id,))
    #     records = self._cursor.fetchall()
    #
    #     return True if int(records[0][0]) == 1 else False

    # def updateExistingRecord(self, table: str, fields: list, values: list) -> bool:
    #     if len(fields) != len(values):
    #         return False
    #
    #     # self._connection = self._connectToDBServer()
    #     # self._cursor = self._connection.cursor(prepared=True)
    #     id_field = fields.pop(0)
    #     id_value = values.pop(0)
    #
    #
    #     current_query: str = self._record_update_query_start
    #     for i, field in enumerate(fields, start=0):
    #         if i == len(fields) - 1:
    #             current_query += f" {field}={values[i]}"
    #         else:
    #             current_query += f" {field}={values[i]},"
    #
    #     current_query += self._record_update_query_end
    #     current_query = current_query.replace('%field', id_field).replace('%value', id_value).replace('%table', table)
    #
    #     print(f"Final update query is: {current_query}")
    #     self._connection = self._connectToDBServer()
    #     self._cursor = self._connection.cursor(prepared=True)
    #
    #     self._cursor.execute(current_query)
    #     if self._cursor.affected_rows < 1:
    #         return False
    #
    #     return True
    def insertRecords(self, table: str, fields: list, values: list) -> bool:
        print(f"Begin populating table {table}")
        # Build insert query
        current_query = self._records_insert_query
        current_query = current_query.replace("%table", table).replace('%fields', ', '.join(fields)).replace('?', ('%s, '*len(values[0]))[0:-2] )

        self._connection = self._connectToDBServer()
        self._cursor = self._connection.cursor(prepared=True)
        # print(current_query)
        try:
            # Inserting each row
            for value_pair in values:
                # Prevent incorrect value for date type field
                value_pair = [None if value == "None" else value for value in value_pair]
                self._cursor.execute(current_query, value_pair)
        # Rollback if something go wrong
        except Exception as e:
            self._connection.rollback()
            print(colorama.Fore.RED + f"Ending populating table {table} with errors: {current_query}" + colorama.Fore.RESET)
            print(colorama.Fore.RED + f"{e}" + colorama.Fore.RESET)
            self.error_count +=1
            return False

        self._connection.commit()
        self._connection.close()
        print(f"Ending populating table {table}")
        return True


    def addFromBackup(self, table_name: str, backup) -> bool:
        print(f"Begin addFromBackup({table_name})")
        fields_infos: list = []
        records: list = []
        for table in backup['tables']:
            if table['name'] == table_name:
                fields_infos = table['fields']
                records = table['records']

        print(colorama.Fore.BLUE + f"{len(records)} records were found for table {table_name}" + colorama.Fore.RESET)

        is_table_created = self.createTable(table_name, fields_infos)

        # If table creation failed or there is no records to insert
        if len(records) == 0 or not is_table_created:
            if len(records) == 0:
                print(colorama.Fore.BLUE + "Table is empty" + colorama.Fore.RESET)
            else:
                print(colorama.Fore.RED + "creation of table went wrong" + colorama.Fore.RESET)
            # print(colorama.Fore.RED + "Table is empty or creation of it went wrong" + colorama.Fore.RESET)
            print(f"End addFromBackup({table_name})")
            return False

        print(colorama.Fore.GREEN + f"Records in table {table_name} found, inserts will start" + colorama.Fore.RESET)
        fields_name: list[str] = [f"`{field_infos['field']}`" for field_infos in fields_infos]
        self.insertRecords(table_name, fields_name, records)
        # # Populating table if there is something in it
        # if len(records) > 0 and is_table_created:
        #     print(colorama.Fore.GREEN + f"Records in table {table_name} found, inserts will start" + colorama.Fore.RESET)
        #     fields_name: list[str] = [f"`{field_infos['field']}`" for field_infos in fields_infos]
        #     self.insertRecords(table_name, fields_name, records)

        print(f"End addFromBackup({table_name})")
        return True

    # def updateFromBackup(self, table: str) -> bool:
    #     print(f"Begin updateFromBackup({table})")
    #     print(f"End updateFromBackup({table})")
    #     return True

    def removeFromDatabase(self, table: str) -> bool:
        print(f"Begin removeFromDatabase({table})")
        self._connection = self._connectToDBServer()
        self._cursor = self._connection.cursor(prepared=True)
        current_query = self._table_drop_query
        try:
            self._cursor.execute(current_query.replace("%table", table))
        except Exception as e:
            print(colorama.Fore.RED + f"{e}" + colorama.Fore.RESET)
            self._connection.close()
            print(f"End removeFromDatabase({table})")
            self._connection.rollback()
            self.error_count +=1
            return False
        self._connection.commit()
        self._connection.close()
        print(f"End removeFromDatabase({table})")
        return True




    def createTable(self, table_name: str, fields_infos) -> bool:
        current_query = self._table_creation_query
        self._connection = self._connectToDBServer()
        self._cursor = self._connection.cursor(prepared=True)
        concat_fields: str = "("
        for field_infos in fields_infos:
            if fields_infos.index(field_infos) + 1 == len(fields_infos):
                concat_fields += self.buildFieldString(field_infos)
            else:
                concat_fields += self.buildFieldString(field_infos) + ", "
        concat_fields += ")"
        try:
            current_query = current_query.replace("%fields", concat_fields).replace("%table", table_name)
            print(f"Query used is: {current_query}")
            self._cursor.execute(current_query)
        except Exception as e:
            print(colorama.Fore.RED + f"{e}" + colorama.Fore.RESET)
            self.error_count +=1
            return False
        return True

    def buildFieldString(self, field_informations) -> str:
        defaultless_types = ['TINYBLOB', 'BLOB', 'MEDIUMBLOB', 'LONGBLOB',
                             'TINYTEXT', 'TEXT', 'MEDIUMTEXT', 'LONGTEXT',
                             'GEOMETRY', 'POLYGON', 'POINT', 'LINESTRING', 'MULTILINESTRING', 'MULTIPOINT', 'MULTIPOLYGON', 'GEOMETRYCOLLECTION'
                             'JSON']
        concat_field = f"`{field_informations['field']}` {field_informations['type'].upper()}"
        if field_informations['key'] == 'PRI' and field_informations['extra'] == 'auto_increment':
            concat_field += " PRIMARY KEY NOT NULL AUTO_INCREMENT"
        elif field_informations['key'] == 'UNI':
            concat_field += " UNIQUE"
        elif field_informations['null'] == 'NO':
            concat_field += " NOT NULL"

        # Add default value if needed (if it's not a blob, a geometry, a json or and text)
        if (field_informations['default'] is not None
                and field_informations['default'] != "" and
                field_informations['type'].upper() not in defaultless_types):
            if 'VARCHAR' in field_informations['type'].upper() or 'CHAR' in field_informations['type'].upper():
                concat_field += f" DEFAULT '{field_informations['default']}'"
            else:
                concat_field += f" DEFAULT {field_informations['default']}"

        print(concat_field)
        return concat_field

    # def deleteTable(self, table: str) -> bool:
    #     self._connection = self._connectToDBServer()
    #     self._cursor = self._connection.cursor(prepared=True)
    #     try:
    #         self._cursor.execute("DROP TABLE IF EXISTS ?", (table,))
    #     except Exception as e:
    #         print(colorama.Fore.RED + f"{e}" + colorama.Fore.RESET)
    #         self.error_count +=1
    #         return False
    #     return True


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







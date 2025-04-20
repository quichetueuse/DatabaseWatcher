from typing import List
import mariadb
from mariadb import Connection
from ConfigManager import ConfigManager
import colorama

class DatabaseManager:

    def __init__(self, config_manager: ConfigManager):
        # Queries used all accross the class
        self._get_dbs_query: str = 'SHOW DATABASES;'
        self._get_tables_query: str = "SHOW TABLES;"
        self._get_fields_query: str = "SHOW FIELDS FROM %table;"
        self._get_records_query: str = "SELECT * FROM %table LIMIT 15;"

        self._records_insert_query: str = "INSERT INTO %table (%fields) VALUES (?)"
        self._record_update_query_start: str = "UPDATE %table SET"
        self._record_update_query_end: str = " WHERE %field=%value"
        self._table_creation_query: str = "CREATE TABLE %table %fields "  # https://www.w3schools.com/sql/sql_foreignkey.asp
        self._database_creation_query: str = "CREATE DATABASE ?;"
        self._table_drop_query: str = "DROP TABLE IF EXISTS %table"
        self._check_record_query: str = "SELECT COUNT(%field) FROM %table WHERE %field=?"

        # Errors during backup creation
        self.table_gathering_error: int = 0
        self.property_gathering_error: int = 0
        self.record_gathering_error: int = 0

        # Errors during backup restoration
        self.table_creation_error: int = 0
        self.table_delete_error: int = 0
        self.record_insert_error: int = 0
        self._config_manager: ConfigManager = config_manager
        self._connection = None
        self._cursor = None

    def _connectToDBServer(self) -> Connection:
        """
        Build connection object and return it
        :return: Connection object
        """
        try:
            conn = mariadb.connect(
                host=self._config_manager.host,
                user=self._config_manager.user,
                password=self._config_manager.password,
                database=self._config_manager.database
            )
            return conn
        except mariadb.OperationalError:
            print(colorama.Fore.RED + "Hostname is not accessible or was mistyped in config file" + colorama.Fore.RESET)
            exit(1)

    def _getAllTables(self) -> List[tuple]:
        """
        Get all tables found in database (given in config file)
        :return: list of all tables found in database
        """
        self._connection = self._connectToDBServer()
        self._cursor = self._connection.cursor()
        tables = None
        try:
            self._cursor.execute(self._get_tables_query)
            tables = self._cursor.fetchall()

        except Exception as e:
            print(colorama.Fore.RED + "Failed to gather tables'")
            print(f"{e}" + colorama.Fore.RESET)
            self.table_gathering_error += 1
        self._connection.close()
        self._cursor = None
        return tables

    def _getFieldsFromTable(self, table: str) -> List[tuple]:
        """
        Get all fields and their properties of a given table
        :param table: name of the table
        :return: list containing all the fields and their properties
        """
        self._connection = self._connectToDBServer()
        self._cursor = self._connection.cursor()
        fields = None
        try:
            self._cursor.execute(self._get_fields_query.replace('%table', table))
            fields = self._cursor.fetchall()
        except Exception as e:
            print(colorama.Fore.RED + f"Failed to gather properties from table '{table}'")
            print(f"{e}" + colorama.Fore.RESET)
            self.property_gathering_error += 1

        self._connection.close()
        self._cursor = None

        return fields

    def _getRecordsFromTable(self, table: str) -> List[tuple]:
        """
        Get every record of a given table
        :param table: name of the table
        :return: list containing all the records
        """
        self._connection = self._connectToDBServer()
        self._cursor = self._connection.cursor(prepared=True)
        records = None
        try:
            self._cursor.execute(self._get_records_query.replace('%table', table))
            records = self._cursor.fetchall()

        except Exception as e:
            print(colorama.Fore.RED + f"Failed to gather records from table '{table}'")
            print(f"{e}" + colorama.Fore.RESET)
            self.record_gathering_error += 1

        self._connection.close()
        self._cursor = None

        return records

    def _insertRecords(self, table: str, fields: list, values: list) -> bool:
        """
        Insert record inside given table
        :param table: name of the table
        :param fields: fields of given table
        :param values: all the values to insert
        :return: Boolean that mean if query worked or not
        """
        print(f"Begin populating table {table}")
        # Build insert query
        current_query = self._records_insert_query
        current_query = current_query.replace("%table", table).replace('%fields', ', '.join(fields)).replace('?', ('%s, '*len(values[0]))[0:-2] )

        self._connection = self._connectToDBServer()
        self._cursor = self._connection.cursor(prepared=True)
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
            self.record_insert_error +=1
            return False

        self._connection.commit()
        self._connection.close()
        print(f"Ending populating table {table}")
        return True


    def addFromBackup(self, table_name: str, backup) -> bool:
        """
        Create table and add records into database (given in config file)
        :param table_name: name of the table
        :param backup: json pattern of given table
        :return: Boolean that mean if query worked or not
        """
        print(f"Begin addFromBackup({table_name})")
        fields_infos: list = []
        records: list = []
        for table in backup['tables']:
            if table['name'] == table_name:
                fields_infos = table['fields']
                records = table['records']

        print(colorama.Fore.BLUE + f"{len(records)} records were found for table {table_name}" + colorama.Fore.RESET)

        is_table_created = self._createTable(table_name, fields_infos)

        # If table creation failed or there is no records to insert
        if len(records) == 0 or not is_table_created:
            if len(records) == 0:
                print(colorama.Fore.BLUE + "Table is empty" + colorama.Fore.RESET)
            else:
                print(colorama.Fore.RED + "creation of table went wrong" + colorama.Fore.RESET)
            print(f"End addFromBackup({table_name})")
            return False

        print(colorama.Fore.GREEN + f"Records in table {table_name} found, inserts will start" + colorama.Fore.RESET)
        fields_name: list[str] = [f"`{field_infos['field']}`" for field_infos in fields_infos]
        self._insertRecords(table_name, fields_name, records)

        print(f"End addFromBackup({table_name})")
        return True

    def removeFromDatabase(self, table: str) -> bool:
        """
        Remove table from database (given in config file)
        :param table: name of the table
        :return: Boolean that mean if query worked or not
        """
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
            self.table_delete_error += 1
            return False
        self._connection.commit()
        self._connection.close()
        print(f"End removeFromDatabase({table})")
        return True

    def _createTable(self, table_name: str, fields_infos) -> bool:
        """
        Create a table into database (given in config file)
        :param table_name: name of the table
        :param fields_infos: json pattern of all the table fields
        :return: Boolean that mean if query worked or not
        """
        current_query = self._table_creation_query
        self._connection = self._connectToDBServer()
        self._cursor = self._connection.cursor(prepared=True)
        concat_fields: str = "("
        # Turn json patterns into fields strings that can be used in the query
        for field_infos in fields_infos:
            if fields_infos.index(field_infos) + 1 == len(fields_infos):
                concat_fields += self._buildFieldString(field_infos)
            else:
                concat_fields += self._buildFieldString(field_infos) + ", "
        concat_fields += ")"
        try:
            # Build query
            current_query = current_query.replace("%fields", concat_fields).replace("%table", table_name)
            print(f"Query used is: {current_query}")
            self._cursor.execute(current_query)
        except Exception as e:
            print(colorama.Fore.RED + f"{e}" + colorama.Fore.RESET)
            self.table_creation_error += 1
            return False
        return True

    def _buildFieldString(self, field_informations) -> str:
        """
        Turn a json pattern into a field string that can be used in a create table query
        :param field_informations: json pattern of a field
        :return: field string
        """
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

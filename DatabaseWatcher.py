from datetime import datetime, date, time
from decimal import Decimal
from typing import List

from ConfigManager import ConfigManager
from DatabaseManager import DatabaseManager
from DumpManager import DumpManager


class DatabaseWatcher:

    def __init__(self, config_file_path):
        # Loading configuration manager class
        self.config_manager = ConfigManager(config_file_path)
        self.crypt_dump = self.config_manager.crypt_dump

        # instancing other app components
        self.database_manager = DatabaseManager(config_manager=self.config_manager)
        self.dump_manager = DumpManager(config_manager=self.config_manager)

    def _createDictionary(self) -> dict:
        """
        Create dictionnary that will be converted into json
        :return: backup dictionnary
        """
        database_dump: dict = {'tables': []}

        # Getting all the tables name in selected database
        tables_name = self._getAllTablesName()

        # Looping through each table
        for table in tables_name:
            # Getting a copy of table pattern
            table_pattern = {"name": None, "fields": [], "records": []}

            # Filling blank pattern
            table_pattern["name"] = table
            # Getting every field information about current table
            table_pattern['fields'] = self._generateFieldPatterns(table=table)
            # Getting every record from current table
            table_pattern['records'] = self._generateRecordPatterns(table=table)

            database_dump['tables'].append(table_pattern)

        return database_dump


    def _generateFieldPatterns(self, table: str) -> List[dict]:
        """
        Build json patterns for field and their properties of given table
        :param table: name of the table
        :return: json pattern for each field of a given table
        """
        # Getting every field from current table
        fields = self.database_manager._getFieldsFromTable(table=table)

        # List that will store all the field patterns
        field_patterns: list[dict] = []

        for field in fields:
            # Getting a copy of field pattern
            field_pattern = {"field": None, "type": None, "null": True, "key": None, "default": None, "extra": None}

            # Filling blank pattern
            for i, pattern_key in enumerate(field_pattern.keys()):
                field_pattern[pattern_key] = field[i]

            # Appending pattern to pattern list
            field_patterns.append(field_pattern)

        return field_patterns

    def _generateRecordPatterns(self, table: str) -> List[list]:
        """
        Build json patterns for records of given table
        :param table: name of the table
        :return: json pattern for each record of a given table
        """
        # Getting every record from current table
        records = self.database_manager._getRecordsFromTable(table=table)

        # List of tuple that will store every record
        record_values: List[list] = []

        # looping through each record fetched from database
        for record in records:
            # Convert every value to string to avoid exception while trying to convert datetime to json
            temporary = [str(value) for value in record]
            record_values.append(temporary)

        return record_values

    def _getAllTablesName(self) -> List[str]:
        """
        Get all tables name
        :return: list containing all the tables name
        """
        raw_tables: List[tuple] = self.database_manager._getAllTables()

        # Getting only tables name
        tables_name: List[str] = [raw_table[0] for raw_table in raw_tables]
        return tables_name

    def compareTables(self):
        """
        Restore backup into database
        """
        # Getting table names from both the backup file and database
        backup = self.dump_manager._GetBackup()
        backup_table_names: list[str] = []
        for table in backup['tables']:
            backup_table_names.append(table['name'])

        db_table_names: list[str] = self._getAllTablesName()
        print(f'current table names: {db_table_names}\n backup table names: {backup_table_names}')

        # Loop through backup tables (to add or update)
        while len(backup_table_names) > 0:
            table = backup_table_names[-1]
            # Add table from backup
            if self._getIndexValueFromList(db_table_names, table) is None:
                print('\nAjout')
                self.database_manager.addFromBackup(table, backup)
                backup_table_names.pop(-1)

            # Update table from backup
            else:
                print('\nupdate')
                self.database_manager.removeFromDatabase(table)
                self.database_manager.addFromBackup(table, backup)
                backup_table_names.pop(-1)
                db_table_names.pop(db_table_names.index(table))

        # Loop through remaining tables from database (to be removed)
        while len(db_table_names) > 0:
            print('\ndelete')
            table = db_table_names[-1]
            # Remove table from database
            self.database_manager.removeFromDatabase(table)
            db_table_names.pop(-1)

        # Show errors to user
        print(f"\n============\nBackup restoring ended with {self.database_manager.table_creation_error + self.database_manager.table_delete_error + self.database_manager.record_insert_error} errors:")
        print(f"\t- {self.database_manager.table_creation_error} table creation error(s)")
        print(f"\t- {self.database_manager.table_delete_error} table delete error(s)")
        print(f"\t- {self.database_manager.record_insert_error} record insert error(s)")

    def _getIndexValueFromList(self, list_to_check: list, value: str):
        """
        Get index of a value in a list
        :param list_to_check: list where the research is done
        :param value: value that need to be found
        :return: Index if found or None
        """
        try:
            result = list_to_check.index(value)
        except ValueError:
            result = None
        return result

    def dumpDatabase(self):
        """
        Create json backup file
        """
        db_dump = self._createDictionary()
        self.dump_manager.writeJsonDump(db_dump, encrypt_dump=self.crypt_dump, file_name=self.config_manager.json_file_name)
        print(f"\n============\nBackup creation ended with {self.database_manager.table_gathering_error + self.database_manager.property_gathering_error + self.database_manager.record_gathering_error} errors:")
        print(f"\t- {self.database_manager.table_gathering_error} table gathering error(s)")
        print(f"\t- {self.database_manager.property_gathering_error} property gathering error(s)")
        print(f"\t- {self.database_manager.record_gathering_error} record gathering error(s)")

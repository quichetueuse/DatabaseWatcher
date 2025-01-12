import json
# from json import dumps
from typing import List

from ConfigManager import ConfigManager
from Cypher import Cypher
from json import dumps, dump

class DumpManager:

    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager

        self.crypt_dump = self.config_manager.crypt_dump

        if self.crypt_dump:
            self.cypher = Cypher()
        else:
            self.cypher = None

    def _toJson(self, database_dump: dict, encrypt_data: bool = False) -> str:
        """
        Method that take à dictionary and convert it to a string in json format
        :param database_dump: Content of the database
        :param encrypt_data: If true json values are not encrypted
        :rtype: str
        :return: Content of the database is json format (in string)
        """

        # If no encryption is needed
        if not encrypt_data:
            return json.dumps(database_dump, indent=2, ensure_ascii=False)

        # if encryption is needed

        # Dictionary that will store encrypted data
        encrypted_database_dump: dict = {"tables": []}

        tables = database_dump.get('tables')
        # Loop through every table
        for table in tables:

            # Blank pattern for database data
            table_pattern = {"name": None, "fields": [], "records": []}

            # Filling pattern with encrypted data
            table_pattern['name'] = self.cypher.encryptString(table['name'])
            table_pattern['fields'] = self._encryptFields(table['fields'])
            table_pattern['records'] = self._encryptRecords(table['records'])
            # print(self.cypher.encryptString(table['name']))

            encrypted_database_dump['tables'].append(table_pattern)

        return json.dumps(encrypted_database_dump, indent=2, ensure_ascii=False)

    def _encryptFields(self, fields: List[dict]) -> List[dict]:

        # List that will store all the field patterns
        field_patterns: list[dict] = []

        for field in fields:
            # Getting a copy of field pattern
            field_pattern = {"field": None, "type": None, "null": True, "key": None, "default": None, "extra": None}

            # Filling blank pattern
            for key in field_pattern.keys():
                field_pattern[key] = self.cypher.encryptString(str(field[key]))

            # Appending pattern to pattern list
            field_patterns.append(field_pattern)

        return field_patterns

    def _encryptRecords(self, records: List[list]) -> List[list]:

        # List of tuple that will store every record
        record_values: List[list] = []

        # looping through each record fetched from database
        for record in records:
            # Convert every value to string to avoid exception while trying to convert datetime to json
            temporary = [self.cypher.encryptString(str(value)) for value in record]
            record_values.append(temporary)

        return record_values

    def writeJsonDump(self, dump_dictionary: dict, file_name: str, encrypt_dump: bool = False):
        json_str = self._toJson(database_dump=dump_dictionary, encrypt_data=encrypt_dump)
        file_name = self._buildFileName(file_name)

        # Writing dump into file
        with (open(file_name, 'w', encoding='utf-8') as json_file):
            json_file.write(json_str)

        return

    def _buildFileName(self, name: str) -> str:
        # If extension in name
        if '.json' in name:
            return name

        return name + '.json'

    def createBackupFile(self, database_dump: dict):
        pass

    def backupDatabase(self, databse_name: str):
        pass

    def restoreDatabase(self, json_path: str):
        pass

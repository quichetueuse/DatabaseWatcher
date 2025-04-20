import json
# from json import dumps
from typing import List

import colorama

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
        Take à dictionary and convert it to a string in json format
        :param database_dump: Content of the database
        :param encrypt_data: If true json values are not encrypted
        :rtype: str
        :return: Content of the database is json format (in string)
        """
        # If no encryption is needed
        if not encrypt_data:
            # print(json.dumps(database_dump, indent=2, ensure_ascii=False))
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

            encrypted_database_dump['tables'].append(table_pattern)

        return json.dumps(encrypted_database_dump, indent=2, ensure_ascii=False)

    def _encryptFields(self, fields: List[dict]) -> List[dict]:
        """
        Encrypt given fields
        :param fields: fields that need to be encrypted
        :return: encrypted field s
        """
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

    def _DecryptFields(self, fields: List[dict]) -> List[dict]:
        """
        Decrypt given field pattern
        :param fields: encrypted fields
        :return: decrypted fields
        """
        # List that will store all the field patterns
        field_patterns: list[dict] = []

        for field in fields:
            # Getting a copy of field pattern
            field_pattern = {"field": None, "type": None, "null": True, "key": None, "default": None, "extra": None}

            # Filling blank pattern
            for key in field_pattern.keys():
                field_pattern[key] = self.cypher.decryptString(field[key])

            # Appending pattern to pattern list
            field_patterns.append(field_pattern)

        return field_patterns

    def _encryptRecords(self, records: List[list]) -> List[list]:
        """
        Encrypt records
        :param records: all the record that need to be encrypted
        :return: list of encrypted records
        """
        # List of tuple that will store every record
        record_values: List[list] = []

        # looping through each record fetched from database
        for record in records:
            # Convert every value to string to avoid exception while trying to convert datetime to json
            temporary = [self.cypher.encryptString(str(value)) for value in record]
            record_values.append(temporary)

        return record_values

    def _DecryptRecords(self, records: List[list]) -> List[list]:
        """
        Decrypt given record pattern
        :param records: encrypted record pattern
        :return: decrypted record pattern
        """
        # List of tuple that will store every record
        record_values: List[list] = []

        # looping through each record fetched from database
        for record in records:
            # Convert every value to string to avoid exception while trying to convert datetime to json
            temporary = [self.cypher.decryptString(value) for value in record]
            record_values.append(temporary)

        return record_values

    def writeJsonDump(self, dump_dictionary: dict, file_name: str, encrypt_dump: bool = False):
        """
        Write json backup in file
        :param dump_dictionary: dictionnary of database to back up
        :param file_name: name of backup file
        :param encrypt_dump: does data need encryption (default is no)
        """
        json_str = self._toJson(database_dump=dump_dictionary, encrypt_data=encrypt_dump)
        file_name = self._buildFileName(file_name)

        # Writing dump into file
        with (open(file_name, 'w', encoding='utf-8') as json_file):
            json_file.write(json_str)

    def readJsonDump(self, file_name) -> dict:
        """
        Read given file and extract the backup content
        :param file_name: file to read
        :return: backup file content as dictionnary
        """
        json_content: dict = {}
        file_name = self._buildFileName(file_name)
        try:
            with (open(file_name, 'r', encoding="utf-8") as json_file):
               json_content = json.load(json_file)
        except FileNotFoundError:
            print(colorama.Fore.RED + f"file '{file_name}' not found, check if the file was moved or delete (also check configuration file)" + colorama.Fore.RESET)
            exit(1)
        return json_content

    def _buildFileName(self, name: str) -> str:
        """
        Add extension to file name if it's missing
        :param name: name of backup file
        :return: proper file name
        """
        # If extension in name
        if '.json' in name:
            return name

        return name + '.json'


    def _DecryptJsonFile(self, json_content: dict) -> dict:
        """
        Decrypt content of json backup file to make it readable
        :param json_content: json backup
        :return: décrypted json backup
        """
        # Dictionary that will store decrypted data
        decrypted_database_dump: dict = {"tables": []}

        tables = json_content.get('tables')
        # Loop through every table
        for table in tables:

            # Blank pattern for database data
            table_pattern = {"name": None, "fields": [], "records": []}
            table_pattern['name'] = self.cypher.decryptString(table['name'])
            table_pattern['fields'] = self._DecryptFields(table['fields'])
            table_pattern['records'] = self._DecryptRecords(table['records'])

            decrypted_database_dump['tables'].append(table_pattern)

        return decrypted_database_dump


    def _GetBackup(self) -> dict:
        """
        Will read json backup file and decrypt it if needed
        :return: json backup as dictionnary
        """
        json_content: dict = self.readJsonDump(self.config_manager.json_file_name)

        # If content need to be decrypted
        if self.crypt_dump:
            decrypted_content: dict = self._DecryptJsonFile(json_content)
            return decrypted_content
        # If content don't need to be decrypted
        return json_content

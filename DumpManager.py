import json


class DumpManager:

    def _toJson(self, database_content: dict, raw: bool = False) -> str:
        """
        Method that take à dictionary and convert it to a string in json format
        :param database_content: Content of the database
        :param raw: If true json values are not encrypted
        :rtype: str
        :return: Content of the database is json format (in string)
        """
        pass

    def _toString(self, database_content: dict, raw: bool = False):
        pass

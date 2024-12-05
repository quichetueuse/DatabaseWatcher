import configparser


class ConfigManager:

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read("config.ini", encoding="utf-8")

        # getting ini sections
        self.main_section = self.config['MAIN']
        self.database_section = self.config['DATABASE']

        # Loading config file content

        self.database = self.database_section.get('db_to_backup')
        self.host = self.database_section.get('db_host')
        self.user = self.database_section.get('db_user')
        self.password = self.database_section.get('db_password')

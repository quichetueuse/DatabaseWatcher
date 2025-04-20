import configparser

import colorama


class ConfigManager:

    def __init__(self, config_file_path: str):
        self.config = configparser.ConfigParser()
        try:
            self.config.read(config_file_path, encoding="utf-8")

            # getting ini sections
            self.main_section = self.config['MAIN']
            self.database_section = self.config['DATABASE']

            # Loading config file content

            # App settings part
            self.crypt_dump = self.main_section.getboolean('crypt_dump')
            self.json_file_name = self.main_section.get('json_file_name')
            self.debug_mode = self.main_section.getboolean('debug_mode')

            # Database part
            self.database = self.database_section.get('db_to_backup')
            self.host = self.database_section.get('db_host')
            self.user = self.database_section.get('db_user')
            self.password = self.database_section.get('db_password')
        except KeyError:
            print(colorama.Fore.RED + f"Configuration file not found (invalid path) or some values are missing in it" + colorama.Fore.RESET)
            exit(1)
        print(colorama.Fore.BLUE + "Configuration loaded" + colorama.Fore.RESET)

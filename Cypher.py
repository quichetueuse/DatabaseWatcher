from cryptography.fernet import Fernet

key = Fernet.generate_key()
class Cypher:

    def encryptDatabaseContent(self, database_content) -> dict:
        encrypted_db_content: dict = {}
        pass

    def decryptDatabaseContent(self, database_content) -> dict:
        encrypted_db_content: dict = {}
        pass

    def _encryptString(self, string: str) -> str:
        # print(key.decode())
        fernet = Fernet(key)
        byte_string = str.encode(string)
        # print(fernet.encrypt(byte_string))
        return str(fernet.encrypt(byte_string))

    def _decryptString(self, string: str) -> str: # todo fusionner encrypt et decrypt dans la meme methode
        fernet = Fernet(key)
        byte_string = str.encode(string)
        # print(fernet.encrypt(byte_string))
        return str(fernet.decrypt(byte_string))


#https://www.tutorialspoint.com/cryptography_with_python/cryptography_with_python_quick_guide.htm

# for value in my_dic.values():
#     del value[:]
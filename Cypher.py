import os
from cryptography.fernet import Fernet


class Cypher:

    def __init__(self):
        encrypt_key: str = os.environ.get('ENC_kEY')
        if encrypt_key is None or encrypt_key == "":
            self.key = Fernet.generate_key()
            os.environ['ENC_KEY'] = self.key.decode()
        print("current encrypt key: ", os.environ['ENC_kEY'])

    def encryptString(self, string: str) -> str:
        fernet = Fernet(self.key)
        byte_string = str.encode(string)
        return fernet.encrypt(byte_string).decode()

    def decryptString(self, string: str) -> str:
        fernet = Fernet(self.key)
        byte_string = str.encode(string)
        return fernet.decrypt(byte_string).decode()

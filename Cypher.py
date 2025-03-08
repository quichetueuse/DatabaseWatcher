import os

from cryptography.fernet import Fernet

# print(os.environ)
#
# encrypt_key: str = os.environ.get('ENC_kEY')
# if encrypt_key is None or encrypt_key == "":
#     key = Fernet.generate_key()
#     os.environ['ENC_KEY'] = str(key)
# print("current encrypt key", os.environ['ENC_kEY'])
# print(os.environ['ENC_KEY'])


class Cypher:

    def __init__(self):
        encrypt_key: str = os.environ.get('ENC_kEY')
        if encrypt_key is None or encrypt_key == "":
            self.key = Fernet.generate_key()
            os.environ['ENC_KEY'] = self.key.decode()
        print("current encrypt key", os.environ['ENC_kEY'])

    def encryptString(self, string: str) -> str:
        # print(key.decode())
        fernet = Fernet(self.key)
        byte_string = str.encode(string)
        # print(fernet.encrypt(byte_string))
        return fernet.encrypt(byte_string).decode()

    def decryptString(self, string: str) -> str: # todo fusionner encrypt et decrypt dans la meme methode
        fernet = Fernet(self.key)
        byte_string = str.encode(string)
        # print(fernet.encrypt(byte_string))
        return fernet.decrypt(byte_string).decode()


#https://www.tutorialspoint.com/cryptography_with_python/cryptography_with_python_quick_guide.htm

# for value in my_dic.values():
#     del value[:]
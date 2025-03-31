import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher,algorithms,modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from passlib.context import CryptContext

class SecurityManager():
    def __init__(self):
        self.kek=base64.b64decode(os.getenv("KEK"))
        if not self.kek:
            raise ValueError("Key Encrypting Key is missing in environment variables")
        self.pass_content=CryptContext(schemes=["bcrypt"],deprecated="auto")
    
    def generate_kek():
        return base64.b64encode(os.urandom(32)).decode()
    
    def generate_dek(self):
        dek=self.encrypt_dek(os.urandom(32))
        return dek

    def encrypt_dek(self,dek: bytes)->str:
        iv=os.urandom(12)
        cipher=Cipher(algorithms.AES(self.kek),modes.GCM(iv),backend=default_backend())
        encrypter=cipher.encryptor()
        encrypted_dek=encrypter.update(dek)+encrypter.finalize()
        return base64.b64encode(iv+encrypter.tag+encrypted_dek).decode()
    
    def decrypt_dek(self,encrypted_dek:str)->bytes:
        encrypted_data=base64.b64decode(encrypted_dek)
        iv,tag,encrypted_dek=encrypted_data[:12],encrypted_data[12:28],encrypted_data[28:]
        cipher=Cipher(algorithms.AES(self.kek),modes.GCM(iv,tag),backend=default_backend())
        decrypter=cipher.decryptor()
        return (decrypter.update(encrypted_dek)+decrypter.finalize()).decode()
    
    def encrypt_secret(self,secret:str,encrypted_dek:str)->str:
        dek=self.decrypt_dek(encrypted_dek)
        iv=os.urandom(12)
        cipher=Cipher(algorithms.AES(dek),modes.GCM(iv),backend=default_backend())
        encrypter=cipher.encryptor()
        encrypted_secret=encrypter.update(secret.encode())+encrypter.finalize()
        return base64.b64encode(iv+encrypter.tag+encrypted_secret).decode()
    
    def decrypt_secret(self,encrypted_secret:str,encrypted_dek:str)->str:
        dek=self.decrypt_dek(encrypted_dek)   
        encrypted_data=base64.b64decode(encrypted_secret)
        iv,tag,encrypted_secret=encrypted_data[:12],encrypted_data[12:28],encrypted_data[28:]
        cipher=Cipher(algorithms.AES(dek),modes.GCM(iv,tag),backend=default_backend())
        decrypter=cipher.decryptor()
        return (decrypter.update(encrypted_secret)+decrypter.finalize()).decode()
    
    def hash_password(self,password:str)->str:
        return self.pass_content.hash(password)
    
    def verify_password(self,password:str,hashed_password:str)->bool:
        return self.pass_content.verify(password,hashed_password)

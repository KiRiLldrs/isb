import os

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes


class Keys:
    @staticmethod
    def generate_symmetric_key(key_length: int)->bytes:
        if key_length not in [128, 192, 256]:
            raise ValueError("Key length for AES must be 128, 192, or 256 bits.")
        return os.urandom(key_length // 8)


    @staticmethod
    def generate_asymmetric_keys()->tuple:
        private_key = rsa.generate_private_key(
            public_exponent = 65537,
            key_size = 2048,
            backend = default_backend()
        )

        return private_key, private_key.public_key()


    @staticmethod
    def serialize_private_key(private_key: rsa.RSAPrivateKey, private_key_path: str)->None:
        with open(private_key_path, "wb") as private_pem:
            private_pem.write(
                private_key.private_bytes(
                    encoding = serialization.Encoding.PEM,
                    format = serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm = serialization.NoEncryption()
                )
            )


    @staticmethod
    def serialize_public_key(public_key: rsa.RSAPublicKey, public_key_path: str)->None:
        with open(public_key_path, "wb") as public_pem:
            public_pem.write(
                public_key.public_bytes(
                    encoding = serialization.Encoding.PEM,
                    format = serialization.PublicFormat.SubjectPublicKeyInfo
                )
            )


    @staticmethod
    def encrypt_symmetric_key(symmetric_key: bytes, public_key: rsa.RSAPublicKey)->bytes:
        encrypted_key = public_key.encrypt(
            symmetric_key,
            padding.OAEP( #Optimal Asymmetric Encryption Padding
                mgf = padding.MGF1(algorithm = hashes.SHA256()),
                algorithm = hashes.SHA256(),
                label = None
            )
        )
        return encrypted_key


    @staticmethod
    def save_encrypted_key(encrypted_key: bytes, path: str)->None:
        with open(path, "wb") as encrypted_file:
            encrypted_file.write(encrypted_key)


    @staticmethod
    def load_private_key(path: str)-> rsa.RSAPrivateKey:
        with open(path, "rb") as key_file:
            return serialization.load_pem_private_key(  # читаем байты и загружаем в объект
                key_file.read(),
                password=None
            )


    @staticmethod
    def load_encrypted_key(path: str)->bytes:
        with open(path, "rb") as enc_file:
             return enc_file.read()


    @staticmethod
    def symmetric_key_decryption(encrypted_key: bytes, private_key: rsa.RSAPrivateKey) -> bytes:
        return private_key.decrypt(
            encrypted_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

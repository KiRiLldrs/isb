import os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding


class FileEncryptor:
    @staticmethod
    def read_file(path: str)->bytes:
        with open(path, "rb") as file:
            return file.read()

    @staticmethod
    def add_padding(data: bytes)->bytes:
        pad = sym_padding.PKCS7(algorithms.AES.block_size).padder()  # если размер текста не кратен 16 добавляем паддинг
        return pad.update(data) + pad.finalize()


    @staticmethod
    def generate_iv()->bytes:
        return os.urandom(16) #инициализирующий вектор


    @staticmethod
    def encrypt_data(data: bytes, key: bytes, iv: bytes)->bytes:
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        encryptor = cipher.encryptor()  # создание шифратора
        return encryptor.update(data) + encryptor.finalize()


    @staticmethod
    def write_encrypted_file(path: str, iv: bytes, cipher_text: bytes)->None:
        with open(path, "wb") as file:
            file.write(iv + cipher_text)



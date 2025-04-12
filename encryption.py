import os

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def symmetric_key_decryption(encrypted_sym_key: str, private_key_path: str)->bytes:
    with open(private_key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key( #читаем байты и загружаем в объект
            key_file.read(),
            password = None
        )

    with open(encrypted_sym_key, "rb") as enc_file:
        enc_key = enc_file.read()

    symmetric_key = private_key.decrypt(
        enc_key,
        padding.OAEP(
            mgf = padding.MGF1(algorithm = hashes.SHA256()),
            algorithm = hashes.SHA256(),
            label = None
        )
    )
    return symmetric_key


def encrypt_file(symmetric_key: bytes, plain_text_path: str, result_path: str)->None:
    with open(plain_text_path, "rb") as file:
        plaintext = file.read()

    pad = sym_padding.PKCS7(algorithms.AES.block_size).padder() #если размер текста не кратен 16 добавляем паддинг
    padded_plaintext = pad.update(plaintext) + pad.finalize()

    iv = os.urandom(16) #инициализирующий вектор

    cipher = Cipher(algorithms.AES(symmetric_key), modes.CBC(iv))
    encryptor = cipher.encryptor() #создание шифратора
    cipher_text = encryptor.update(padded_plaintext) + encryptor.finalize()

    with open(result_path, "wb") as file:
        file.write(iv + cipher_text)

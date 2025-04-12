from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding


def file_decryption(encrypted_file_path: str, symmetric_key: bytes, output_path: str)->None:
    with open(encrypted_file_path, "rb") as file:
        data = file.read()
        iv = data[:16]
        cipher_text = data[16:]

    cipher = Cipher(algorithms.AES(symmetric_key), modes.CBC(iv))
    decryptor  = cipher.decryptor() #Создание дешифратора
    padded_text = decryptor.update(cipher_text) + decryptor.finalize() #дешифрованный текст со служебными байтами

    unpadder = sym_padding.PKCS7(algorithms.AES.block_size).unpadder() #заполнение последнего блока до полного размера
    text = unpadder.update(padded_text) + unpadder.finalize() #удаление лишних байт

    with open(output_path, "wb") as file:
        file.write(text)
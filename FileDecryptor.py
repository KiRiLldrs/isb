from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding


class FileDecryptor:
    @staticmethod
    def read_encrypted_file(path: str)->tuple[bytes, bytes]:
        with open(path, "rb") as file:
            data = file.read()
            return data[:16], data[16:]


    @staticmethod
    def decrypt_data(cipher_text: bytes, key: bytes, iv: bytes)->bytes:
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        decryptor = cipher.decryptor()  # Создание дешифратора
        return decryptor.update(cipher_text) + decryptor.finalize() #дешифрованный текст со служебными байтами


    @staticmethod
    def remove_padding(padded_data: bytes)->bytes:
        unpadder = sym_padding.PKCS7(algorithms.AES.block_size).unpadder()  # заполнение последнего блока до полного размера
        return unpadder.update(padded_data) + unpadder.finalize()  # удаление лишних байт


    @staticmethod
    def write_decrypted_file(path: str, data: bytes)->None:
        with open(path, "wb") as file:
            file.write(data)

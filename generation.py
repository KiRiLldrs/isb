import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding


def generate_symmetric_key(key_length: int)->bytes:
    if key_length not in [128, 192, 256]:
        raise ValueError("Key length for AES must be 128, 192, or 256 bits.")
    return os.urandom(key_length // 8)


def generate_asymmetric_keys()->tuple:
    private_key = rsa.generate_private_key(
        public_exponent = 65537,
        key_size = 2048,
        backend = default_backend()
    )

    public_key = private_key.public_key()
    return private_key, public_key


def serialize(private_key: rsa.RSAPrivateKey, public_key: rsa.RSAPublicKey,
              private_key_path: str, public_key_path: str)->None:
    with open(private_key_path, "wb") as private_pem:
        private_pem.write(
            private_key.private_bytes(
                encoding = serialization.Encoding.PEM,
                format = serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm = serialization.NoEncryption()
            )

        )

    with open(public_key_path, "wb") as public_pem:
        public_pem.write(
            public_key.public_bytes(
                encoding = serialization.Encoding.PEM,
                format = serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )


def encrypt_symmetric_key(symmetric_key: bytes, public_key: rsa.RSAPublicKey, encrypted_symmetric_path: str)->None:
    encrypted_key = public_key.encrypt(
        symmetric_key,
        padding.OAEP( #Optimal Asymmetric Encryption Padding
            mgf = padding.MGF1(algorithm = hashes.SHA256()),
            algorithm = hashes.SHA256(),
            label = None
        )
    )

    with open(encrypted_symmetric_path, "wb") as encrypted_file:
        encrypted_file.write(encrypted_key)

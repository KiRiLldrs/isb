from const import (
    ENCRYPTED_SYMMETRIC_KEY,
    PUBLIC_KEY,
    PRIVATE_KEY,
    PLAINTEXT,
    ENCRYPTED_TEXT,
    DECRYPTED_TEXT
)
import generation
import encryption
import decryption


def main():
    sym_key = generation.generate_symmetric_key(128)
    private_key, public_key = generation.generate_asymmetric_keys()

    generation.serialize(private_key, public_key, PRIVATE_KEY, PUBLIC_KEY)
    generation.encrypt_symmetric_key(sym_key, public_key, ENCRYPTED_SYMMETRIC_KEY)

    encryption.encrypt_file(
        encryption.symmetric_key_decryption(ENCRYPTED_SYMMETRIC_KEY, PRIVATE_KEY),
        PLAINTEXT, ENCRYPTED_TEXT
    )

    decryption.file_decryption(ENCRYPTED_TEXT,
                               encryption.symmetric_key_decryption(ENCRYPTED_SYMMETRIC_KEY, PRIVATE_KEY),
                               DECRYPTED_TEXT
                               )


if __name__ == "__main__":
    main()
from cryptography.fernet import Fernet


def encrypt_image(data):
    symmetric_key = Fernet.generate_key()
    cipher_fernet = Fernet(symmetric_key)

    cipherdata = cipher_fernet.encrypt(data)



    return symmetric_key, cipherdata
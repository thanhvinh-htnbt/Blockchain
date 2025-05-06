from cryptography.fernet import Fernet


def decrypt_image(symmetric_key, data):
    cipher_fernet = Fernet(symmetric_key)
    decrypted_data = cipher_fernet.decrypt(data)

    return decrypted_data
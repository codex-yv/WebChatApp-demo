from cryptography.fernet import Fernet


def encryptt(chat:str):

    encoded_statement = chat.encode()
    key = Fernet.generate_key()
    encryptor = Fernet(key)
    token = encryptor.encrypt(encoded_statement)

    return key, token


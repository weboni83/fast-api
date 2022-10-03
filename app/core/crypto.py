import string
import bcrypt


def encryption(password: string):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password

def decryption(hashed_password: string):
    save_password = hashed_password.decode('utf-8')
    return save_password

def checkpw(input_password: string, save_password: string):
    is_correct = bcrypt.checkpw(input_password.encode('utf-8'),save_password)
    return is_correct
import string
import bcrypt


def encryption(password: string):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password

def checkpw(input_password: string, save_password: string):
    is_correct = bcrypt.checkpw(input_password.encode('utf-8'),save_password.encode('utf-8'))
    return is_correct
import os
from passlib.hash import pbkdf2_sha256
from dotenv import load_dotenv


load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')


def hash_password(plain_password):
    return pbkdf2_sha256.hash(SECRET_KEY + plain_password)


def verify_passwor(plain_password, hashed_password):
    return pbkdf2_sha256.verify(SECRET_KEY + plain_password, hashed_password)

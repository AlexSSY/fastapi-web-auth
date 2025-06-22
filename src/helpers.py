import secrets
from passlib.hash import pbkdf2_sha256
from . import db, config


def hash_password(plain_password):
    return pbkdf2_sha256.hash(config.SECRET_KEY + plain_password)


def verify_password(plain_password, hashed_password):
    return pbkdf2_sha256.verify(config.SECRET_KEY + plain_password, hashed_password)


def authenticate(username, password):
    user_class = config.get_user_class()
    username_field = getattr(user_class, config.USERNAME_FIELD_NAME)
    with db.SessionLocal() as session:
        user = session.query(user_class).where(username_field == username).first()
        if user is not None and verify_password(password, user.password_hash):
            return user, secrets.token_hex(16)
    return None, None

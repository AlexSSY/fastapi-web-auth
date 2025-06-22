import os
from importlib import import_module
from dotenv import load_dotenv


load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
USER_MODEL = 'src.models.User'
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
COOKIE_NAME = "session_token"
USERNAME_FIELD_NAME = 'email'


_user_class = None
def get_user_class():
    global _user_class
    if _user_class is None:
        split = USER_MODEL.split('.')
        class_name = split.pop()
        module_name = '.'.join(split)

        module = import_module(module_name)
        _user_class = getattr(module, class_name)
    return _user_class

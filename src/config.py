import os
from importlib import import_module
from dotenv import load_dotenv


load_dotenv()
USER_MODEL = 'src.models.User'
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')


def get_user_class():
    split = USER_MODEL.split('.')
    class_name = split.pop()
    module_name = '.'.join(split)

    module = import_module(module_name)
    return getattr(module, class_name)

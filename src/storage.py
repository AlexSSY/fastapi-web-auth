import redis
from . import config


r = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)


def store(key, value):
    r.set(key, value)


def retrieve(key):
    return r.get(key)

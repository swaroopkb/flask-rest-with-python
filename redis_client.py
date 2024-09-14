from redis import Redis
from flask import current_app, jsonify


def get_redis_client():
    if "redis_client" not in current_app.extensions:
        redis_client = Redis(
            host=current_app.config.get("REDIS_HOST", "redis"),
            port=current_app.config.get("REDIS_PORT", 6379),
            db=current_app.config.get("REDIS_DB", 0),
            decode_responses=True,
        )
        current_app.extensions["redis_client"] = redis_client
    return current_app.extensions["redis_client"]


def set_redis_value(key, value):
    redis_client = get_redis_client()
    redis_client.set(key, value)
    return jsonify({"message": f"Set {key} o {value}"})


def get_redis_value(key):
    redis_client = get_redis_client()
    value = redis_client.get(key)
    return value

import os
import json
import random
from typing import Any
from redis import Redis, ConnectionPool
from redis.exceptions import RedisError

REDIS_URL = os.getenv("REDIS_URL")
CACHE_TTL_S = int(os.getenv("CACHE_TTL_SECONDS"))

redis_pool = ConnectionPool.from_url(
    REDIS_URL,
    decode_responses = True, #so we get back a string, not bytes
    max_connections = 20,
    socket_connect_timeout = 5,
    socket_timeout = 5,
    retry_on_timeout = True,
    health_check_interval = 30
)

redis_client = Redis(connection_pool = redis_pool)
def get_redis(): #fast API dependency
    return redis_client 

def get_cache(client: Redis, key: str):
    try:
        raw = client.get(key) #an attempt to fetch the data from the key
    except RedisError:
        return None
    
    if raw is None:
        return None
    
    try:
        return json.loads(raw) #trying to convert the JSON sting -> python dict
    except json.JSONDecodeError: #when data is not a valid JSON
        return None

def set_cache(client: Redis, key: str, value: Any, ttl: int = CACHE_TTL_S, jitter: int = 30):
    expire = ttl + random.randint(0, jitter)
    client.setex(key, expire, json.dumps(value)) # json.dumps(): py dict -> single string of text that Redis can easily store

def delete_cache(client: Redis, *keys: str):
    if not keys:
        return 
    client.delete(*keys)
#!/usr/bin/env python3
"""
Module to define a Cache class for storing data in Redis.
"""
import redis
import uuid
from typing import Callable, Union


class Cache:
    """
    A class for storing data in Redis.

    Attributes:
    _redis (redis.Redis): A Redis connection object.
    """

    def __init__(self) -> None:
        """
        Initialize the Cache object and flush the Redis database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in the Redis database.

        Args:
        data (Union[str, bytes, int, float]): The data to be stored.

        Returns:
        str: The key under which the data is stored.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

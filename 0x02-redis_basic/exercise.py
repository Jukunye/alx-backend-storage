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

    def get(self,
            key: str,
            fn: Callable = None
            ) -> Union[str, bytes, int, float]:
        """
        Get a value from Redis by key,
        with an optional transformation function.

        Args:
            key: The key to retrieve the value for.
            fn: An optional transformation function
                to apply to the retrieved value.

        Returns:
            The retrieved value,
            optionally transformed by the provided function.
        """
        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_str(self, key: str) -> str:
        """
        Get a string value from Redis by key.
        """
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """
        Get an integer value from Redis by key.
        """
        return self.get(key, lambda x: int(x))

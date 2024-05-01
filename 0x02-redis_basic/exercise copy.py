#!/usr/bin/env python3
"""
Module to define a Cache class for storing data in Redis.
"""
import redis
import uuid
from typing import Callable, Union
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator tracks the number of calls made to a method in a Cache class.
    """
    mkey = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Invokes the given method after incrementing its call counter.
        """
        self._redis.incr(mkey)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """stores the input and output history of a method in a Redis list."""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrap the decorated function"""
        input = str(args)
        self._redis.rpush(method.__qualname__ + ":inputs", input)
        output = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ":outputs", output)
        return output
    return wrapper


def replay(fn: Callable):
    """
    Display the history of calls for a particular function.

    Args:
        fn: The function to replay.

    Returns:
        None
    """
    r = redis.Redis()
    func_name = fn.__qualname__
    call_count = r.get(func_name)
    try:
        call_count = int(call_count.decode("utf-8"))
    except (AttributeError, ValueError):
        call_count = 0

    print("{} was called {} times:".format(func_name, call_count))
    inputs = r.lrange("{}:inputs".format(func_name), 0, -1)
    outputs = r.lrange("{}:outputs".format(func_name), 0, -1)

    for inp, outp in zip(inputs, outputs):
        inp_str = inp.decode("utf-8") if isinstance(inp, bytes) else ""
        outp_str = outp.decode("utf-8") if isinstance(outp, bytes) else ""
        print("{}(*{}) -> {}".format(func_name, inp_str, outp_str))


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

    @call_history
    @count_calls
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

        Args:
            key: The key to retrieve the string value for.

        Returns:
            The string value retrieved from Redis.
        """
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """
        Get an integer value from Redis by key.

        Args:
            key: The key to retrieve the integer value for.

        Returns:
            The integer value retrieved from Redis.
        """
        return self.get(key, lambda x: int(x))

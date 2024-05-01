#!/usr/bin/env python3
"""This module contains the function get_page"""
import requests
import redis
from functools import wraps

r = redis.Redis()


def counter(method):
    """adds counting and caching functionality to the decorated function."""
    @wraps(method)
    def wrapper(url):
        cached_key = "cached:" + url
        cached_data = r.get(cached_key)
        if cached_data:
            return cached_data.decode("utf-8")

        count_key = "count:" + url
        html = method(url)

        r.incr(count_key)
        r.set(cached_key, html)
        r.expire(cached_key, 10)
        return html
    return wrapper


@counter
def get_page(url: str) -> str:
    """
    Fetches the content of a URL using requests and returns it as a string.
    """
    return requests.get(url).text

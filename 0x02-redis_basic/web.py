#!/usr/bin/env python3
'''A module with tools for request caching and tracking.
'''
import redis
import requests
from functools import wraps
from typing import Callable


redis_store = redis.Redis()
'''
A Redis client for caching and tracking requests.

'''


def data_cacher(method: Callable) -> Callable:
    '''
    A decorator for caching the output of a function.
    Args:
        method (Callable): The function to cache the output for.
    Returns:
        Callable: The decorated function with caching.
    '''
    @wraps(method)
    def invoker(url) -> str:
        '''
        Checks if the result of the request is cached
        and returns it if available.
        If not, makes the request, caches the result,
        and returns it.
        Args:
            url (str): The URL of the request.
        Returns:
            str: The content of the URL if available,
            or the result of the request.
        '''
        redis_store.incr(f'count:{url}')
        result = redis_store.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        redis_store.set(f'count:{url}', 0)
        redis_store.setex(f'result:{url}', 10, result)
        return result
    return invoker


@data_cacher
def get_page(url: str) -> str:
    '''
    Makes a GET request to the given URL
    and returns its content.
    Args:
        url (str): The URL of the request.
    Returns:
        str: The content of the URL.
    '''
    return requests.get(url).text

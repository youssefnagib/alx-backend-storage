#!/usr/bin/env python3
"""
A simple in-memory cache using Redis.
"""
import redis
import requests
from functools import wraps
from typing import Callable

redis_store = redis.Redis()

def data_cacher(method: Callable) -> Callable:
    """
    A decorator for caching the output of a function and tracking the count.
    
    Args:
        method (Callable): The function to cache the output for.
    
    Returns:
        Callable: The decorated function with caching.
    """
    @wraps(method)
    def invoker(url: str) -> str:
        """
        Checks if the result of the request is cached and returns it if available.
        If not, makes the request, caches the result, and returns it.
        
        Args:
            url (str): The URL of the request.
        
        Returns:
            str: The content of the URL if available, or the result of the request.
        """
        count_key = f'count:{url}'

        redis_store.incr(count_key)
        count = redis_store.get(count_key).decode("utf-8")
        
        print(f"Request count for {url}: {count}")
        
        key = url
        data = redis_store.get(key)

        if data:
            return data.decode("utf-8")

        cache = method(url)
        redis_store.setex(key, 10, cache)
        return cache
    
    return invoker


@data_cacher
def get_page(url: str) -> str:
    """
    Makes a GET request to the given URL and returns its content.
    
    Args:
        url (str): The URL of the request.
    
    Returns:
        str: The content of the URL.
    """
    response = requests.get(url)
    return response.text

'''Test'''
if __name__ == "__main__":
    url = "http://google.com"
    print(get_page(url))

#!/usr/bin/env python3
'''
A simple in-memory cache using Redis.
'''
import redis
from typing import Union, Optional, Callable
import uuid


class Cache:
    def __init__(self) -> None:
        '''Initializes a Cache instance.
        '''
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores the given data in Redis and returns a unique key for it.

        Args:
            data (Union[bytes, int, float]): The data to store.

        Returns:
            str: The unique key for the stored data.
        """
        dataKey = str(uuid.uuid4())
        self._redis.set(dataKey, data)
        return dataKey

    def get(self,
            key: str,
            fn: Optional[Callable] = None,
            ) -> Union[str, bytes, int, float, None]:
        '''
        Retrieves the data associated with the given key from Redis.
        Args:
            key (str): The unique key for the data to retrieve.
            fn (Optional[Callable], optional): A function to apply
            to the retrieved data. Defaults to None.
        Returns:
            Union[str, bytes, int, float, None]: The retrieved data
            or None if the key does not exist.
        '''
        data = self._redis.get(key)

        if data is None:
            return None

        if fn:
            callable_fn = fn(data)
            return callable_fn
        else:
            return data

    def get_str(self, key: str) -> str:
        '''
        Retrieves the string representation of the data
        associated with the given key from Redis.
        Args:
            key (str): The unique key for the data to retrieve.
        Returns:
            str: The string representation of the retrieved data.
        '''
        value = self._redis.get(key, fn=lambda d: d.decode('utf-8'))
        return value

    def get_int(self, key: str) -> int:
        ''''''
        value = self._redis.get(key)
        try:
            value = int(value.decode('utf-8'))
        except Exception:
            return None
        return value

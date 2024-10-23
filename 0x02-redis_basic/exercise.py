#!/usr/bin/env python3
'''
A simple in-memory cache using Redis.
'''
import redis
from typing import Union
import uuid


class Cache:
    def __init__(self) -> None:
        '''Initializes a Cache instance.
        '''
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    def store(self, data: Union[bytes, int, float]) -> str:
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

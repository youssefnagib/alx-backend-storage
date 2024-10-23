#!/usr/bin/env python3
'''
A simple in-memory cache using Redis.
'''
import redis
from typing import Union, Optional, Callable, Any
import uuid
from functools import wraps


def count_calls(method: Callable) -> Callable:
    '''
    Increments the call counter of a method stored in Redis.
    Args:
        method (Callable): The method to count the calls for.
    Returns:
        Callable: The decorated method with call counter incrementing.
    '''
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        '''Invokes the given method after incrementing its call counter.
        '''
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return invoker


def call_history(method: Callable) -> Callable:
    '''
    Records the call history of a method stored in Redis.
    Args:
        method (Callable): The method to record the call history for.
    Returns:
        Callable: The decorated method with call history recording.
    '''
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        '''
        Records the input and output of the given method in Redis.
        Args:
            *args: Input arguments.
            **kwargs: Input keyword arguments.
        Returns:
            The output of the given method.
        '''
        inKey = '{}:inputs'.format(method.__qualname__)
        outKey = '{}:outputs'.format(method.__qualname__)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(inKey, str(args))
        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(outKey, output)
        return output
    return invoker


def replay(fn: Callable) -> None:
    '''
    Replays the call history of a method stored in Redis.
    Args:
        fn (Callable): The method to replay.
    Returns:
        None. Prints the call history of the method.
    '''
    if fn is None or not hasattr(fn, '__self__'):
        return
    redis_store = getattr(fn.__self__, '_redis', None)
    if not isinstance(redis_store, redis.Redis):
        return
    fxn_name = fn.__qualname__
    inKey = '{}:inputs'.format(fxn_name)
    outKey = '{}:outputs'.format(fxn_name)
    fxn_call_count = 0
    if redis_store.exists(fxn_name) != 0:
        fxn_call_count = int(redis_store.get(fxn_name))
    print('{} was called {} times:'.format(fxn_name, fxn_call_count))
    fxn_inputs = redis_store.lrange(inKey, 0, -1)
    fxn_outputs = redis_store.lrange(outKey, 0, -1)
    for fxn_input, fxn_output in zip(fxn_inputs, fxn_outputs):
        print('{}(*{}) -> {}'.format(
            fxn_name,
            fxn_input.decode("utf-8"),
            fxn_output,
        ))


class Cache:
    def __init__(self) -> None:
        '''Initializes a Cache instance.
        '''
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
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
        '''
        Retrieves the integer representation of the data
        associated with the given key from Redis.
        Args:
            key (str): The unique key for the data to retrieve.
        Returns:
            int: The integer representation of the retrieved data.
            None: If the data is not a valid integer.
        '''
        value = self._redis.get(key)
        try:
            value = int(value.decode('utf-8'))
        except Exception:
            return None
        return value

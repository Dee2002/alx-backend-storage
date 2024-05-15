#!/usr/bin/env python3
import redis
import uuid
from typing import Union, Callable, Optional
import functools


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of times a method is called.

    Args:
        method (Callable): The method to decorate.

    Returns:
        Callable: The decorated method.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """Increment the call count and call the original method."""
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs of a function.

    Args:
        method (Callable): The method to decorate.

    Returns:
        Callable: The decorated method.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """Store the input and output history of the function call."""
        input_key = method.__qualname__ + ":inputs"
        output_key = method.__qualname__ + ":outputs"
        self._redis.rpush(input_key, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(result))
        return result
    return wrapper


class Cache:
    """Cache class for basic Redis operations."""

    def __init__(self):
        """Initialize the Cache instance."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the given data in Redis and return the generated key.

        Args:
            data (Union[str, bytes, int, float]): The data to store.

        Returns:
            str: The generated key.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
        self,
        key: str,
        fn: Optional[Callable] = None
    ) -> Union[str, bytes, int, float, None]:
        """
        Retrieve data from Redis and optionally apply a conversion function.

        Args:
            key (str): The key to retrieve.
            fn (Optional[Callable]): The conversion function to apply.

        Returns:
            Union[str, bytes, int, float, None]: The retrieved data.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve a string value from Redis.

        Args:
            key (str): The key to retrieve.

        Returns:
            Optional[str]: The retrieved string or None.
        """
        data = self.get(key, lambda d: d.decode('utf-8'))
        return data

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve an integer value from Redis.

        Args:
            key (str): The key to retrieve.

        Returns:
            Optional[int]: The retrieved integer or None.
        """
        data = self.get(key, lambda d: int(d))
        return data


def replay(method: Callable):
    """
    Display the history of calls of a particular function.

    Args:
        method (Callable): The function to display history for.
    """
    input_key = method.__qualname__ + ":inputs"
    output_key = method.__qualname__ + ":outputs"
    redis_instance = method.__self__._redis

    inputs = redis_instance.lrange(input_key, 0, -1)
    outputs = redis_instance.lrange(output_key, 0, -1)

    print(f"{method.__qualname__} was called {len(inputs)} times:")
    for input_data, output_data in zip(inputs, outputs):
        print(f"{method.__qualname__}(*{input_data.decode('utf-8')}) -> "
              f"{output_data.decode('utf-8')}")

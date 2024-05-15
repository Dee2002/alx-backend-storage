#!/usr/bin/env python3
import requests
import redis
from typing import Callable


redis_instance = redis.Redis()


def count_calls(method: Callable) -> Callable:
    """Decorator to count the number of times a URL is accessed."""

    def wrapper(url: str) -> str:
        """Wrapper function to increment the access count and
        call the method."""
        redis_instance.incr(f"count:{url}")
        return method(url)
    return wrapper


@count_calls
def get_page(url: str) -> str:
    """
    Get the HTML content of a URL and cache it with an expiration time.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The HTML content of the URL.
    """
    cached_content = redis_instance.get(url)
    if cached_content:
        return cached_content.decode('utf-8')

    response = requests.get(url)
    html_content = response.text
    redis_instance.setex(url, 10, html_content)
    return html_content


if __name__ == "__main__":
    url =
    "http://slowwly.robertomurray.co.uk/delay/3000/url/http://www.example.com"
    print(get_page(url))
    print(get_page(url))  # Should fetch from cache

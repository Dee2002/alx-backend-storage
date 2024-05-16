#!/usr/bin/env python3
import requests
import redis
from typing import Callable

# Initialize Redis instance
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
    # Check if the content is cached in Redis
    cached_content = redis_instance.get(url)
    if cached_content:
        return cached_content.decode('utf-8')

    # If not cached, fetch the content from the URL
    response = requests.get(url)

    # Check if the response is successful
    if response.status_code == 200:
        html_content = response.text
        # Cache the content in Redis with a 10-second expiration
        redis_instance.setex(url, 10, html_content)
        return html_content
    else:
        # If the request fails, return an error message
        return f"Error: Failed to fetch content from {url}"


if __name__ == "__main__":
    # Example usage
    url = "http://slowwly.robertomurray.co.uk"
    print(get_page(url))  # Fetches the content (may take a few seconds)
    print(get_page(url))  # Fetches from cache (instantaneous)

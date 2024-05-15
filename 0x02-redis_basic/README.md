# Redis Basic

This project demonstrates basic usage of Redis for caching and tracking method calls using Python.

## Installation

1. **Install Redis on Ubuntu 18.04**

    ```sh
    $ sudo apt-get -y install redis-server
    $ pip3 install redis
    $ sudo sed -i "s/bind .*/bind 127.0.0.1/g" /etc/redis/redis.conf
    ```

2. **Start Redis server**

    ```sh
    $ sudo service redis-server start
    ```

3. **Install required Python packages**

    ```sh
    $ pip3 install redis
    ```

## Usage

1. **Run the main script**

    ```sh
    $ python3 main.py
    ```

    This will store some data in Redis, print the stored keys, and display the call history of the `store` method.

2. **Run the web cache script**

    ```sh
    $ python3 web.py
    ```

    This will demonstrate caching web pages and tracking URL access counts.

## Project Structure

- `exercise.py`: Contains the `Cache` class with methods to store, retrieve, and track data in Redis.
- `main.py`: Demonstrates the usage of the `Cache` class and the `replay` function.
- `web.py`: Contains the `get_page` function to cache web pages and track access counts.
- `README.md`: Project documentation.

## Functionality

- **Cache class**
  - `store(data)`: Stores the given data in Redis and returns a generated key.
  - `get(key, fn)`: Retrieves data from Redis and optionally applies a conversion function.
  - `get_str(key)`: Retrieves a string value from Redis.
  - `get_int(key)`: Retrieves an integer value from Redis.

- **Decorators**
  - `count_calls`: Counts the number of times a method is called.
  - `call_history`: Stores the history of inputs and outputs of a function.

- **Utility Function**
  - `replay(method)`: Displays the history of calls of a particular function.

- **Web Cache**
  - `get_page(url)`: Fetches the HTML content of a URL, caches it in Redis with a 10-second expiration, and tracks the number of accesses.

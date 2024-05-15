#!/usr/bin/env python3
""" Main file """

from exercise import Cache, replay

cache = Cache()

# Store some values
s1 = cache.store("first")
print(s1)
s2 = cache.store("second")
print(s2)
s3 = cache.store("third")
print(s3)

# Retrieve and print call history for store method
inputs = cache._redis.lrange(f"{cache.store.__qualname__}:inputs", 0, -1)
outputs = cache._redis.lrange(f"{cache.store.__qualname__}:outputs", 0, -1)

print("inputs: {}".format(inputs))
print("outputs: {}".format(outputs))

# Replay the history of calls for the store method
replay(cache.store)

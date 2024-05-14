#!/usr/bin/env python3

from typing import List


def list_all(mongo_collection) -> List:
    """ lists all documents in a collection """
    documents = mongo_collection.find()
    return [doc for doc in documents]

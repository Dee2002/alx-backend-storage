#!/usr/bin/env python3


def insert_school(mongo_collection, **kwargs):
    """ inserts a new document in a collection based on kwargs """
    document = mongo_collection.insert(kwargs)
    return document

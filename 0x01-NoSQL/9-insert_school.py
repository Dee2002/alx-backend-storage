#!/usr/bin/env python3
"""
Insert a document in a collection
"""

def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document in a collection based on kwargs
    Args:
        mongo_collection: pymongo collection object
        **kwargs: key-value pairs to insert
    Returns:
        The _id of the new document
    """
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id

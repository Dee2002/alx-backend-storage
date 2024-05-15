#!/usr/bin/env python3
"""
List all documents in a collection
"""

def list_all(mongo_collection):
    """
    Lists all documents in a collection
    Args:
        mongo_collection: pymongo collection object
    Returns:
        List of documents, empty list if no document in collection
    """
    if mongo_collection.count_documents({}) == 0:
        return []
    return list(mongo_collection.find())

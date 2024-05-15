#!/usr/bin/env python3
"""
Module to return top students sorted by average score
"""


def top_students(mongo_collection):
    """
    Function that returns all students sorted by average score
    """
    pipeline = [
        {
            "$project": {
                "name": 1,
                "averageScore": {
                    "$avg": "$topics.score"
                }
            }
        },
        {
            "$sort": {
                "averageScore": -1
            }
        }
    ]
    return list(mongo_collection.aggregate(pipeline))

#!/usr/bin/env python3
"""
This module contains the function top_students.
"""


def top_students(mongo_collection):
    """returns all students sorted by average score"""
    return mongo_collection.aggregate([
        {"$project": {
            "name": "$name",
            "averageScore": {"$avg": "$topics.score"}
            }},
        {"$sort": {"averageScore": -1}}
    ])

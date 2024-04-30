#!/usr/bin/env python3
"""
This module contains the function schools_by_topic.
"""
import pymongo


def schools_by_topic(mongo_collection, topic):
    """returns the list of school having a specific topic"""
    return mongo_collection.find({"topics": topic})

#!/usr/bin/env python3
"""
This module contains a function that list all document
"""


def list_all(mongo_collection):
    """
    list all collections
    """
    if not mongo_collection:
        return []
    return list(mongo_collection.find())

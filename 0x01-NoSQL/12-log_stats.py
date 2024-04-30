#!/usr/bin/env python3
"""
This module  provides some stats about Nginx logs stored in MongoDB
"""
from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    log_collection = client.logs.nginx

    http_methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {}

    for method in http_methods:
        method_counts[method] = log_collection.count_documents(
            {"method": method})

    query = {"path": "/status", "method": "GET"}
    status_documents = log_collection.count_documents(query)
    total_documents = log_collection.count_documents({})

    print("{} logs".format(total_documents))
    print("Methods:")
    for method, count in method_counts.items():
        print("\tmethod {}: {}".format(method, count))
    print("{} status check".format(status_documents))

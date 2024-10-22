#!/usr/bin/env python3
'''
update topics task 10
'''


def update_topics(mongo_collection, name, topics):
    mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )

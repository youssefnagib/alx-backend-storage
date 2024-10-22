#!/usr/bin/env python3
'''
update topics task 10
'''


def update_topics(mongo_collection, name, topics) -> None:
    '''
    Update the topics for a given school
    :param mongo_collection: MongoCollection object
    :param name: name of the school
    :param topics: list of new topics
    :return: None
    '''
    mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )

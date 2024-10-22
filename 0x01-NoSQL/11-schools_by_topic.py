#!/usr/bin/env python3
'''
schools by topic task 11
'''


def schools_by_topic(mongo_collection, topic):
    '''
    Get schools with a given topic
    :param mongo_collection: MongoCollection object
    :param topic: topic to search for
    :return: list of schools that match the topic
    '''
    topicFilter = {
        "topics": {
            '$elemMatch': {
                '$eq': topic,
            },
        },
    }
    return [schools for schools in mongo_collection.find(topicFilter)]


#!/usr/bin/env python3
'''
list all task 8
'''


def list_all(mongo_collection):
    '''
    List all documents in the collection
    :param mongo_collection: MongoCollection object
    :return: list of documents
    '''
    return list(school for school in mongo_collection.find())

#!/usr/bin/env python3
'''
insert a new school document task 9
'''


def insert_school(mongo_collection, **kwargs):
    '''
    Insert a new school document into the collection
    :param mongo_collection: MongoCollection object
    :param kwargs: keyword arguments representing the school document
     :return: the id of the inserted document
     '''
    inserts = mongo_collection.insert_one(kwargs)
    return inserts.inserted_id

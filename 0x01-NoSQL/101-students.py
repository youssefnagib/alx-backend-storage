#!/usr/bin/env python3
'''Task 101'''


def top_students(mongo_collection):
    '''
    Get the top students based on their average score
    :param mongo_collection: MongoCollection object
    :return: list of students with their average score sorted in descending order
    '''
    students = mongo_collection.aggregate(
        [
            {
                '$project': {
                    '_id': 1,
                    'name': 1,
                    'averageScore': {
                        '$avg': {
                            '$avg': '$topics.score',
                        },
                    },
                    'topics': 1,
                },
            },
            {
                '$sort': {'averageScore': -1},
            },
        ]
    )
    return students
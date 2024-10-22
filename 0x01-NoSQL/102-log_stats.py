#!/usr/bin/env python3
'''
task 12
'''
from pymongo import MongoClient


def print_nginx_request_logs(nginx_collection) -> None:
    '''
    Print Nginx request logs
    :param nginx_collection: MongoCollection object
    :return: None
    '''
    print('{} logs'.format(nginx_collection.count_documents({})))
    print('Methods:')
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    for method in methods:
        method_count = len(list(nginx_collection.find({'method': method})))
        print('\tmethod {}: {}'.format(method, method_count))
    status_checks_count = len(list(
        nginx_collection.find({'method': 'GET', 'path': '/status'})
    ))
    print('{} status check'.format(status_checks_count))

def print_top_ips(server_collection) -> None:
    '''
    Print top 10 IP addresses with the highest number of requests
    '''
    print('IPs:')
    top_requests = server_collection.aggregate(
        [
            {
                '$group': {'_id': "$ip", 'totalRequests': {'$sum': 1}}
            },
            {
                '$sort': {'totalRequests': -1}
            },
            {
                '$limit': 10
            },
        ]
    )
    for request in top_requests:
        ip = request['_id']
        ip_requests_count = request['totalRequests']
        print('\t{}: {}'.format(ip, ip_requests_count))


def run():
    '''
    run mongodb
    '''
    client = MongoClient('mongodb://127.0.0.1:27017')
    print_nginx_request_logs(client.logs.nginx)
    print_top_ips(client.logs.nginx)


if __name__ == '__main__':
    run()

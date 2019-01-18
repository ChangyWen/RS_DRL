#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from read_data import *
from global_parameters import set_value, GRID_NUMS

def cal_requests(data:pd.DataFrame):
    '''
    :param data: the dataframe from read_trips_data
    :return: dict, request[grid_id][time_slot] = [list of requests]
    '''
    REQUEST = {}
    for d in range(1, 31 + 1):
        REQUEST[d] = {}
        for t in range(60 * 24):
            REQUEST[d][t] = {}
            for g in range(1, GRID_NUMS + 1):
                REQUEST[d][t][g] = []

    data_DTG = data.groupby(['day','pickup_time','PULocationID'])
    for key, group in data_DTG:
        REQUEST[key[0]][key[1]][key[2]].append(group.index.tolist())
    set_value('REQUEST', REQUEST)
    return REQUEST

def requests_to_file(REQUEST, file_name):
    json_str = json.dumps(REQUEST)
    with open(file_name, 'w') as json_file:
        json_file.write(json_str)

def gen_requests(data:pd.DataFrame):
    REQUEST = cal_requests(data)
    requests_to_file(REQUEST, 'request_dict/request_dict.json')

# data = read_trip_data('trip_data/yellow_tripdata_2018-06.csv')
# gen_requests(data)

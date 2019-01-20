#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle
from read_data import *
from global_parameters import GRID_NUMS

def cal_requests(data:pd.DataFrame):
    '''
    :param data: the dataframe from read_request_data
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
    return REQUEST

def requests_to_file(REQUEST, file_name):
    file = open(file_name, 'wb')
    pickle.dump(REQUEST, file)
    file.close()
    # with open(file_name, 'wb') as json_file:
    #     json_file.write(temp)

def gen_requests(data:pd.DataFrame):
    REQUEST = cal_requests(data)
    requests_to_file(REQUEST, 'request_dict/request_dict.pkl')

data = read_request_data('trip_data/filtered_yellow_tripdata_2018-06.csv')
gen_requests(data)

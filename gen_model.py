#!/usr/bin/env python
# -*- coding: utf-8 -*-
from read_data import *
from sys import maxsize
from global_parameters import GRID_NUMS
'''
    generate fare model from grid to grid according to the NYC dataset
'''
def cal_model(data:pd.DataFrame):
    '''
    :param grouped_dict: the trip data set
    :return: a fare model indicate the fee from grid to grid
    '''
    FARE = np.zeros(shape=[GRID_NUMS + 1, GRID_NUMS + 1], dtype=np.float)
    DISTANCE = np.zeros(shape=[GRID_NUMS + 1, GRID_NUMS + 1], dtype=np.float)
    DISTANCE -= 1
    TRAVEL_TIME = np.zeros(shape=[24, GRID_NUMS + 1, GRID_NUMS + 1], dtype=np.int)
    data_PD = data.groupby(['PULocationID', 'DOLocationID'])
    for key, group in data_PD:
        FARE[key[0]][key[1]] = group['fare_amount'].mean(axis=0)
        if len(group) == 0:
            DISTANCE[key[0]][key[1]] = maxsize
        else:
            DISTANCE[key[0]][key[1]] = group['trip_distance'].mean(axis=0)
        data_S = group.groupby('hour')
        for key_s, group_s in data_S:
            TRAVEL_TIME[key_s][key[0]][key[1]] = int(group_s['travel_time'].mean(axis=0))
    return FARE, DISTANCE, TRAVEL_TIME

def model_to_file(FARE, DISTANCE, TRAVEL_TIME, file_name):
    np.savetxt(file_name[0], FARE, fmt='%f', delimiter = ',')
    np.savetxt(file_name[1], DISTANCE, fmt='%f', delimiter = ',')
    np.savetxt(file_name[2], TRAVEL_TIME.reshape([TRAVEL_TIME.size]).tolist(), fmt='%d', delimiter=',')

def gen_model(data:pd.DataFrame):
    FARE, DISTANCE, TRAVEL_TIME = cal_model(data)
    file_name = []
    file_name.append('models/fare_model/fare_model.csv')
    file_name.append('models/distance_model/distance_model.csv')
    file_name.append('models/travel_time_model/driving_time_model.csv')
    model_to_file(FARE, DISTANCE, TRAVEL_TIME, file_name)

# gen_model(read_filtered_data('trip_data/filtered_yellow_tripdata.csv'))


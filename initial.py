#!/usr/bin/env python
# -*- coding: utf-8 -*-

from global_parameters import *
import pickle
import pandas as pd
from util import *
def initialize():
    '''
    initialize fare, distance, travel_time model
                requests, vehicles
    '''
    with open('models/fare_model/fare_model.csv', 'rb') as fare_file:
        fare = np.loadtxt(fname=fare_file,
                          delimiter=",",
                      skiprows=0,)
    with open('models/distance_model/distance_model.csv', 'rb') as distance_file:
        distance = np.loadtxt(fname=distance_file,
                              delimiter=",",
                              skiprows=0)
    with open('models/travel_time_model/driving_time_model.csv') as travel_time_file:
        travel_time = np.loadtxt(fname=travel_time_file,
                                 delimiter=",",
                                 skiprows=0)
        travel_time = travel_time.reshape([24, GRID_NUMS + 1, GRID_NUMS + 1])
    with open('request_dict/request_dict.pkl', 'rb') as request_file:
        request = pickle.load(request_file)
        REQUESTS = {}
        DATA = get_value('Data')
        for key1 in request.keys():
            for key2 in request[key1].keys():
                for key3 in request[key1][key2].keys():
                    for index in request[key1][key2][key3]:
                        request_ins = Request(r_id=index,
                                              day=DATA.loc[index, 'day'],
                                              time=DATA.loc[index, 'pickup_time'],
                                              origin=DATA.loc[index, 'PULocation'],
                                              destination=DATA.loc[index, 'DOLocationID'],
                                              count=DATA.loc[index, 'passenger_count']
                                              )
                        REQUESTS[index] = request_ins
        set_value('REQUESTS', REQUESTS)
    with open('vehicles_df/vehicles_df.csv', 'rb') as vehicle_file:
        vehicle = pd.read_csv(vehicle_file,
                              na_filter=False,
                              usecols=['vehicle_ID',
                                       'start_loc',
                                       'start_time',
                                       'stop_time',
                                       ],
                              dtype={'vehicle_ID':np.int,
                                     'start_loc':np.int,
                                     'start_time':np.int,
                                     'stop_time':np.int,
                                     },
                              nrows=VEHICLES_NUMS,
                              )
        VEHICLES = []
        for i in range(len(vehicle)):
            vehicle_ins = Vehicle(v_id=vehicle.loc[i,'vehicle_ID'],
                                  location=vehicle.loc[i, 'start_loc'],
                                  start_time=0,
                                  stop_time=vehicle.loc[i, 'stop_time'])
            VEHICLES.append(vehicle_ins)
    return fare, distance, travel_time, request, VEHICLES
    ### Reduce to N and M
# initialize()
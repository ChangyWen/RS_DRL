#!/usr/bin/env python
# -*- coding: utf-8 -*-

from global_parameters import *
import pickle
import pandas as pd

def initialize():
    '''
    initialize fare, distance, travel_time model
                requests, vehicles
    '''
    with open('models/fare_model/fare_model.csv', 'rb') as fare_file:
        FARE = np.loadtxt(fname=fare_file,
                          delimiter=",",
                      skiprows=0,)
    with open('models/distance_model/distance_model.csv', 'rb') as distance_file:
        DISTANCE = np.loadtxt(fname=distance_file,
                              delimiter=",",
                              skiprows=0)
    with open('models/travel_time_model/driving_time_model.csv') as travel_time_file:
        TRAVEL_TIME = np.loadtxt(fname=travel_time_file,
                                 delimiter=",",
                                 skiprows=0)
        TRAVEL_TIME = TRAVEL_TIME.reshape([24, GRID_NUMS + 1, GRID_NUMS + 1])
    with open('request_dict/request_dict.pkl', 'rb') as request_file:
        REQUEST = pickle.load(request_file)
    with open('vehicles_df/vehicles_df.csv', 'rb') as vehicle_file:
        VEHICLE = pd.read_csv(vehicle_file,
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
                              )
    set_value('FARE', FARE)
    set_value('DISTANCE', DISTANCE)
    set_value('TRAVEL_TIME', TRAVEL_TIME)
    set_value('REQUEST', REQUEST)

initialize()
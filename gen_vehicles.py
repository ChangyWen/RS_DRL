#!/usr/bin/env python
# -*- coding: utf-8 -*-

from global_parameters import *
import pandas as pd

def cal_vehicles():
    data = pd.DataFrame(columns=('vehicle_ID',
                                 'start_loc',
                                 'start_time',
                                 'stop_time',
                                 )
                      )
    for i in range(1, VEHICLES_NUMS + 1):
        start_loc = np.random.randint(1, GRID_NUMS)
        start_time = int(np.random.triangular(0, 8 * 60, 24 * 60))
        temp = start_time + np.random.randint(8 * 60, 12 * 60)
        stop_time = temp if temp < 1440 else temp - 1440
        data.loc[i] = [i, start_loc, start_time, stop_time]
    return data

def vehicles_to_file(data, file_name):
    data.to_csv(file_name, index=False, header=True)

def gen_vehicles():
    data = cal_vehicles()
    vehicles_to_file(data, 'vehicles_df/vehicles_df.csv')

# gen_vehicles()
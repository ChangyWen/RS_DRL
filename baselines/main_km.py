#!/usr/bin/env python
# -*- coding: utf-8 -*-


from baselines import KM
from read_data import read_request_data
import initial
from global_parameters import set_value

if __name__ == "__main__":
    DATA = read_request_data('trip_data/filtered_yellow_tripdata_2018-06.csv')
    KM.KM_mapping()
    set_value('DATA', DATA)
    print('point1: initialize begin')
    request_all = initial.initialize()
    print('point2: initialize end')
    set_value('request_all', request_all)
    total_r = KM.KM_run()
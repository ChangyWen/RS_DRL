#!/usr/bin/env python
# -*- coding: utf-8 -*-


# import tensorflow as tf
import numpy as np

### True if network structure wanted, False otherwise ###
OUTPUT_GRAPH = False
### The directory storing the log file of the network (shown in tensorboard) ###
LOG_DIR = './network_log'
### The name of the global_net ###
GLOBAL_NET_SCOPE = 'Global_Net'
### A_BOUND = [low, high] ###
A_BOUND = []
MAX_DETOUR_TIME = 25
GRID_NUMS = 265
REQUEST_NUMS = 3000
VEHICLES_NUMS = 10000 # 13,586

global_dict = {'SESS':None,
               'OPT_A':None,
               'OPT_C':None,
               'GlOBAL_RUNNING_R':[],
               'GLOBAL_EP':0,
               'COORD':None,
               'DATA':None,
               'REQUESTS':None,
               'VEHICLES':None,
               'request_all':None,
               'travel_time':None,
               'fare':None,
               'shortest_dis':None,
               'predecessors':None,
               }

def set_value(name, value):
    global global_dict
    if name not in global_dict.keys():
        print('Set value error: undefined key')
        return
    global_dict[name] = value

def get_value(name, defValue=None):
    try:
        return global_dict[name]
    except KeyError:
        return defValue

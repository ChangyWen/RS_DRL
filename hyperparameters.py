#!/usr/bin/env python
# -*- coding: utf-8 -*-

import multiprocessing

### True if network structure wanted, False otherwise ###
OUTPUT_GRAPH = False

### The directory storing the log file of the network (shown in tensorboard) ###
LOG_DIR = './network_log'

N_WORKERS = multiprocessing.cpu_count()

### The time_step = 5 mins ###
TIME_STEP = 5

### Maximum steps in one episode ###
MAX_EP_STEP = 24 * 60 / TIME_STEP

### Maximum learning episode ###
MAX_GLOBAL_EP = 2000

### The name of the global_net ###
GLOBAL_NET_SCOPE = 'Global_Net'

### The #iteration in local_net before push_operation ###
UPDATE_GLOBAL_ITER = 10

### discount factor ###
GAMMA = 0.9

### The weight of the entropy ###
ENTROPY_BETA = 0.01

### Learning rate for actor ###
LR_A = 0.0001

### Learning rate for critic ###
LR_C = 0.001

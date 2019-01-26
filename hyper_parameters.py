#!/usr/bin/env python
# -*- coding: utf-8 -*-

import multiprocessing
import tensorflow as tf
from global_parameters import VEHICLES_NUMS, REQUEST_NUMS

N_WORKERS = 2 # multiprocessing.cpu_count()

### The time_step = 5 mins ###
TIME_STEP = 1

### Maximum steps in one episode ###
MAX_EP_STEP = int(24 * 60 / TIME_STEP)

### Maximum learning episode ###
MAX_GLOBAL_EP = 20

### The #iteration in local_net before push_operation ###
UPDATE_GLOBAL_ITER = 10

### Exponentially weighted average factor ###
EWA_BETA = (UPDATE_GLOBAL_ITER - 1) / UPDATE_GLOBAL_ITER

### discount factor ###
GAMMA = 0.9

### The weight of the entropy ###
ENTROPY_BETA = 0.01

### Learning rate for actor ###
LR_A = 0.0001

### Learning rate for critic ###
LR_C = 0.001

### dimension of state and action ###
N_S = REQUEST_NUMS * 3 + VEHICLES_NUMS * 2 + 2
N_A = VEHICLES_NUMS * REQUEST_NUMS

### initialization of weights in network ###
W_INIT = tf.truncated_normal_initializer(0., .1)

UNIT_A = 128
UNIT_C = 64

N_Rider = None ## ?
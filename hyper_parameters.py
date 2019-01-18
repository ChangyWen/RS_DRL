#!/usr/bin/env python
# -*- coding: utf-8 -*-

import multiprocessing
import tensorflow as tf

N_WORKERS = multiprocessing.cpu_count()

### The time_step = 5 mins ###
TIME_STEP = 5

### Maximum steps in one episode ###
MAX_EP_STEP = 24 * 60 / TIME_STEP

### Maximum learning episode ###
MAX_GLOBAL_EP = 2000

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
N_S = 0
N_A = 0

### initialization of weights in network ###
W_INIT = tf.random_normal_initializer(0., .1)

UNIT_A = 256
UNIT_C = 128

N_Rider = None ## ?
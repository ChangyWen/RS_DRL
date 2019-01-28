#!/usr/bin/env python
# -*- coding: utf-8 -*-

from munkres import Munkres, print_matrix, make_cost_matrix, DISALLOWED
from sys import maxsize
from baselines import non_rl_env
from hyper_parameters import MAX_EP_STEP, MAX_GLOBAL_EP
from global_parameters import VEHICLES_NUMS, REQUEST_NUMS, get_value, MAX_DETOUR_TIME
import numpy as np

def cal_profit(REQUESTS, VEHICLES, request_selected, vehicle, current_time):
    current_hour = int(current_time / 60)
    profit_matrix = np.zeros(shape = [VEHICLES_NUMS, REQUEST_NUMS])
    travel_time = get_value('travel_time')
    fare = get_value('fare')
    for i in range(len(vehicle)):
        for j in range(len(request_selected)):
            ve = vehicle[i]
            re = request_selected[j]
            if re == -1:
                continue
            if travel_time[current_hour][VEHICLES[ve].location][REQUESTS[re].origin] < MAX_DETOUR_TIME \
                    and REQUESTS[re].count <= VEHICLES[ve].cap - VEHICLES[ve].load:
                cost = fare[VEHICLES[ve].location][REQUESTS[re].origin] * 0.1
                fee = fare[REQUESTS[re].origin][REQUESTS[re].destination]
                profit_matrix[i][j] = (fee - cost) if fee > cost else 0
        return profit_matrix


def KM_mapping(REQUESTS, VEHICLES, request_selected, vehicle, current_time):
    profit_matrix = cal_profit(REQUESTS, VEHICLES, request_selected, vehicle, current_time)
    km_weights = make_cost_matrix(profit_matrix, lambda item: (maxsize - item) if item != 0 else DISALLOWED)
    m = Munkres()
    indexes = m.compute(km_weights)
    total = 0
    for row, column in indexes:
        value = profit_matrix[row][column]
        total += value
    return indexes, total

def KM_run(REQUESTS, VEHICLES):
    env = non_rl_env.RideSharing_Env()
    day = 1
    global_ep = 0
    total_r = 0
    while global_ep < MAX_GLOBAL_EP:
        request_selected, vehicle = env.reset(day)
        ep_r = 0
        for ep_t in range(MAX_EP_STEP):
            action, reward = KM_mapping(REQUESTS, VEHICLES, request_selected, vehicle, ep_t)
            ep_r += reward
            request_selected, vehicle, done = env.step(action)
            if done:
                break
        total_r += ep_r
    return total_r

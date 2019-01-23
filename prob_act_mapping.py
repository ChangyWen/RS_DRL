#!/usr/bin/env python
# -*- coding: utf-8 -*-

from munkres import Munkres, print_matrix, make_cost_matrix, DISALLOWED
from sys import maxsize
import numpy as np
from global_parameters import VEHICLES_NUMS, REQUEST_NUMS, get_value, MAX_DETOUR_TIME


def cal_profit(request_selected, vehicle, current_time):
    REQUESTS = get_value('REQUESTS')
    VEHICLES = get_value('VEHICLES')
    profit_matrix = np.zeros(shape=[VEHICLES_NUMS, REQUEST_NUMS]) # N * M
    travel_time = get_value('travel_time')
    fare = get_value('fare')
    for i in range(len(vehicle)):
        for j in range(len(request_selected)):
            ve = vehicle[i]
            re = request_selected[j]
            if travel_time[current_time][VEHICLES[ve].location][REQUESTS[re].origin] < MAX_DETOUR_TIME:
                cost = fare[VEHICLES[ve].location][REQUESTS[re].origin] * 0.1
                fee = fare[REQUESTS[re].origin][REQUESTS[re].destination]
                profit_matrix[i][j] = (fee - cost) if fee > cost else 0
    return profit_matrix

def KM_mapping(action, request_selected, vehicle, current_time): # ?????
    '''
    :param prob_weights: a_prob
    :return: matching final action,"indexes":
    '''
    # prob_weights = [5, DISALLOWED, 70, 0,
    #           10, 3, 2, 3,
    #           9, DISALLOWED, 4, 5,
    #             1,2,3,4,
    #                 90,5,1,DISALLOWED]
    profit_matrix = cal_profit(request_selected, vehicle, current_time)
    km_matrix = profit_matrix * action
    km_weights = make_cost_matrix(km_matrix, lambda item: (maxsize - item) if item != 0 else DISALLOWED)
    # matrix = np.array(prob_weights)
    # matrix = np.reshape(matrix, [VEHICLES_NUMS, REQUEST_NUMS])
    # matrix = matrix.transpose()
    # cost_matrix = make_cost_matrix(matrix, lambda cost: (maxsize - cost) if (cost != DISALLOWED) else DISALLOWED)
    m = Munkres()
    indexes = m.compute(km_weights)
    print_matrix(profit_matrix, msg='Highers profit through this matrix:')
    total = 0
    for row, column in indexes:
        # print(row, column)
        value = profit_matrix[row][column]
        total += value
        # print('(%d, %d) -> %d' % (row, column, value))
        # print('total profit: %d' % total)
    return indexes, total
# KM_mapping([])
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from munkres import Munkres, print_matrix, make_cost_matrix, DISALLOWED
from sys import maxsize
import numpy as np

def KM_mapping(action): # ?????
    '''
    :param prob_weights: a_prob
    :return: matching final action,"indexes":
    '''
    prob_weights = [5, DISALLOWED, 70, 0,
              10, 3, 2, 3,
              9, DISALLOWED, 4, 5,
                1,2,3,4,
                    90,5,1,DISALLOWED]
    matrix = np.array(prob_weights)
    matrix = np.reshape(matrix, [5,4])
    # matrix = matrix.transpose()
    cost_matrix = make_cost_matrix(matrix, lambda cost: (maxsize - cost) if (cost != DISALLOWED) else DISALLOWED)
    m = Munkres()
    indexes = m.compute(cost_matrix)
    print_matrix(matrix, msg='Highers profit through this matrix:')
    total = 0
    for row, column in indexes:
        print(row, column)
        value = matrix[row][column]
        total += value
        print('(%d, %d) -> %d' % (row, column, value))
        print('total profit: %d' % total)
    total = total # ????
    return indexes, total
# KM_mapping([])
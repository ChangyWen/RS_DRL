#!/usr/bin/env python
# -*- coding: utf-8 -*-

from munkres import Munkres, print_matrix, make_cost_matrix, DISALLOWED
from sys import maxsize
import numpy as np
def KM_mapping():
    '''
    :param prob_weights: list of
    :return: matching final action
    '''
    matrix = [5, DISALLOWED, 1, 0,
              10, 3, 2, 3,
              9, DISALLOWED, 4, 5]
    matrix = np.array(matrix)
    matrix = np.reshape(matrix, [3,4])
    cost_matrix = make_cost_matrix(matrix, lambda cost: (maxsize - cost) if (cost != DISALLOWED) else DISALLOWED)
    m = Munkres()
    indexes = m.compute(cost_matrix)
    print_matrix(matrix, msg='Lowest cost through this matrix:')
    total = 0
    for row, column in indexes:
        print(row, column)
        value = matrix[row][column]
        total += value
        print('(%d, %d) -> %d' % (row, column, value))
        print('total cost: %d' % total)
KM_mapping()
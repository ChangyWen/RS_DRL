#!/usr/bin/env python
# -*- coding: utf-8 -*-

### global total reward for observation ###
GLOBAL_RUNNING_R = []

### global learning episode ###
GLOBAL_EP = 0

class Worker(object):
    '''
    Class: Worker of AcNet work [job: def work()] in parallel
    '''
    def __init__(self, name, globalAC):
        '''
        :param name: worker's name
        :param globalAC: worker's global_net's name
        '''
        pass

    def work(self):
        '''
        The job of the the Workers
        '''
        pass
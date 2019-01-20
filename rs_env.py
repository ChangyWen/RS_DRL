#!/usr/bin/env python
# -*- coding: utf-8 -*-



class RideSharing_Env(object):
    '''
    Class: The environment of ride-sharing;
            Interact with A3C learning;
    '''
    def __init__(self):
        '''
        initialize the vehicles, orders data into variables
        '''

        pass

    def step(self, action = None):
        '''
        :param action: The action to be taken
        :return:
            -> state_: the next state after action
            -> reward: the immediate reward of taking action
            -> done: flag, true if state_ = terminal and false otherwise
            -> info: information needed
        '''
        reward = 0
        state_ = None
        done = False
        info = None
        return state_, reward, done, info

    def reset(self):
        '''
        Reset the environment after terminal state
        :return:
            -> state: an new initial state
        '''
        state = None
        return state

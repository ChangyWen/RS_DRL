#!/usr/bin/env python
# -*- coding: utf-8 -*-

import initial
import random
from global_parameters import *

class RideSharing_Env(object):
    '''
    Class: The environment of ride-sharing;
            Interact with A3C learning;
    '''

    def __init__(self):
        '''
        initialize the vehicles,...
        '''
        self.fare, self.distance, self.travel_time, self.request_all, self.VEHICLES = initial.initialize()
        # self.request = None
        self.vehicle = []
        self.day = 0
        self.REQUESTS = get_value('REQUESTS')

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

    def reset(self, day):
        '''
        Reset the environment after terminal state, reset to the next day with time = 0
        :return:
            -> state: an new initial state
        '''
        self.day = day
        request_selected = []
        request_state = []
        vehicle_state = []
        '''
            select M requests
        '''
        for grid in self.request_all[day][0].keys():
            request_selected += self.request_all[day][0][grid]
        if day > 1:
            for grid in self.request_all[day-1].keys():
                for time in range(1410, 1440):
                    for grid in self.request_all[day-1][time].keys():
                        request_selected += self.request_all[day-1][time][grid]
        if len(request_selected) > REQUEST_NUMS:
            request_selected = random.sample(request_selected, REQUEST_NUMS)
        else:
            request_selected += ([-1] * REQUEST_NUMS - len(request_selected))
        for index in range(request_selected):
            if index != -1:
                request_state += [self.REQUESTS[index].origin,
                                  self.REQUESTS[index].destination,
                                  self.REQUESTS[index].count]
            else:
                request_state += [0, 0, 0]
        '''
            select N vehicles
        '''
        for i in range(len(self.VEHICLES)):
            if self.VEHICLES[i].stop_time < self.VEHICLES[i].start_time or self.VEHICLES[i].start_time == 0:
                self.VEHICLES[i].serving = 1
                self.vehicle.append(i)
                vehicle_state += [self.VEHICLES[i].location, self.VEHICLES[i].cap - self.VEHICLES[i].load]
        state = np.concatenate(([self.day], [0], request_state, vehicle_state))
        return state
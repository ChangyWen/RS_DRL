#!/usr/bin/env python
# -*- coding: utf-8 -*-

import initial
import random
from global_parameters import *
from prob_act_mapping import KM_mapping

class RideSharing_Env(object):
    '''
    Class: The environment of ride-sharing;
            Interact with A3C learning;
    '''

    def __init__(self):
        '''
        initialize the vehicles,...
        '''
        self.request_all = initial.initialize()
        # self.request = None
        self.vehicle = []
        self.day = 0
        self.time = 0
        self.request_selected = []
        self.REQUESTS = get_value('REQUESTS')
        self.VEHICLES = get_value('VEHICLES')

    def step(self, action = None):
        '''
        :param action: The action to be taken
        :return:
            -> state_: the next state after action
            -> reward: the immediate reward of taking action
            -> done: flag, true if state_ = terminal and false otherwise
            -> info: information needed
        '''
        final_action, reward = KM_mapping(action, self.request_selected, self.vehicle, self.time)
        for ve, re in final_action:
            self.VEHICLES[ve].pick_up.append(self.request_selected[re])
            re_day = self.REQUESTS[self.request_selected[re]].day
            re_time = self.REQUESTS[self.request_selected[re]].time
            re_grid = self.REQUESTS[self.request_selected[re]].origin
            self.request_all[re_day][re_time][re_grid].remove(self.request_selected[re])
            self.VEHICLES[ve].load += self.REQUESTS[self.request_selected[re]].count
            self.REQUESTS[self.request_selected[re]].served = 1
            self.VEHICLES[ve].update_route()
        self.request_selected = []
        request_state = []
        vehicle_state = []
        self.time += 1
        if self.time == 1440:
            done = True
            info = None
            return [0] * (REQUEST_NUMS * 3), reward, done, info
        for grid in self.request_all[self.day][self.time].keys():
            self.request_selected += self.request_all[self.day][self.time][grid]
        if self.day > 1 and self.time < 30:
            for grid in self.request_all[self.day-1].keys():
                for time in range(1440 + self.time - 30, 1440):
                    for grid in self.request_all[self.day-1][time].keys():
                        self.request_selected += self.request_all[self.day-1][time][grid]
        else:
            for grid in self.request_all[self.day].keys():
                for time in range(self.time - 30, self.time):
                    for grid in self.request_all[self.day-1][time].keys():
                        self.request_selected += self.request_all[self.day-1][time][grid]
        if len(self.request_selected) > REQUEST_NUMS:
            self.request_selected = random.sample(self.request_selected, REQUEST_NUMS)
        else:
            self.request_selected += ([-1] * REQUEST_NUMS - len(self.request_selected))
        for index in range(self.request_selected):
            if index != -1:
                request_state += [self.REQUESTS[index].origin,
                                  self.REQUESTS[index].destination,
                                  self.REQUESTS[index].count]
            else:
                request_state += [0, 0, 0]
        '''
            select N vehicles, vehicle_state consider the next grid the car going to ???
        '''
        for i in range(len(self.VEHICLES)):
            if (self.VEHICLES[i].stop_time < self.VEHICLES[i].start_time and self.VEHICLES[i].stop_time >= self.time) \
                    or (self.VEHICLES[i].start_time <= self.time and self.VEHICLES[i].stop_time >= self.time):
                if self.VEHICLES[i].load < self.VEHICLES[i].cap:
                    self.VEHICLES[i].serving = 1
                    self.vehicle.append(i)
                    vehicle_state += [self.VEHICLES[i].location, self.VEHICLES[i].cap - self.VEHICLES[i].load]
            else:
                vehicle_state += [0, 0]
        state_ = np.concatenate(([self.day], [0], request_state, vehicle_state))
        done = False if self.time < 1439 else True
        info = None
        return state_, reward, done, info

    def reset(self, day):
        '''
        Reset the environment after terminal state, reset to the next day with time = 0
        :return:
            -> state: an new initial state
        '''
        self.day = day
        self.time = 0
        self.request_selected = []
        request_state = []
        vehicle_state = []
        '''
            select M requests
        '''
        for grid in self.request_all[day][0].keys():
            self.request_selected += self.request_all[day][0][grid]
        if self.day > 1:
            for grid in self.request_all[day-1].keys():
                for time in range(1410, 1440):
                    for grid in self.request_all[day-1][time].keys():
                        self.request_selected += self.request_all[day-1][time][grid]
        if len(self.request_selected) > REQUEST_NUMS:
            self.request_selected = random.sample(self.request_selected, REQUEST_NUMS)
        else:
            self.request_selected += ([-1] * REQUEST_NUMS - len(self.request_selected))
        for index in range(self.request_selected):
            if index != -1:
                request_state += [self.REQUESTS[index].origin,
                                  self.REQUESTS[index].destination,
                                  self.REQUESTS[index].count]
            else:
                request_state += [0, 0, 0]
        '''
            select N vehicles, vehicle_state consider the next grid the car going to ???
        '''
        for i in range(len(self.VEHICLES)):
            if self.VEHICLES[i].stop_time < self.VEHICLES[i].start_time or self.VEHICLES[i].start_time == 0:
                if self.VEHICLES[i].load < self.VEHICLES[i].cap:
                    self.VEHICLES[i].serving = 1
                    self.vehicle.append(i)
                    vehicle_state += [self.VEHICLES[i].location, self.VEHICLES[i].cap - self.VEHICLES[i].load]
            else:
                vehicle_state += [0, 0]
        state = np.concatenate(([self.day], [0], request_state, vehicle_state))
        return state
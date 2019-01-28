#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
from global_parameters import *
import random

class RideSharing_Env(object):
    def __init__(self):
        self.vehicle = []
        self.day = 0
        self.time = 0
        self.request_selected = []
        self.request_all = copy.deepcopy(get_value('request_all'))
        self.REQUESTS = copy.deepcopy(get_value('REQUESTS'))
        self.VEHICLES = copy.deepcopy(get_value('VEHICLES'))

    def step(self, action):
        # a = [0] * (VEHICLES_NUMS * REQUEST_NUMS)
        for i, j in action:
            ve = self.vehicle[i]
            re = self.request_selected[j]
            # a[i * REQUEST_NUMS + j] = 1
            self.VEHICLES[ve].pick_up.append(self.request_selected[re])
            re_day = self.REQUESTS[self.request_selected[re]].day
            re_time = self.REQUESTS[self.request_selected[re]].time
            re_grid = self.REQUESTS[self.request_selected[re]].origin
            if self.VEHICLES[ve].location == re_grid:
                self.VEHICLES[ve].onboard.append(self.request_selected[re])
                self.REQUESTS[self.request_selected[re]].pu_t = self.time
                self.VEHICLES[ve].load += self.REQUESTS[self.request_selected[re]].count
            self.request_all[re_day][re_time][re_grid].remove(self.request_selected[re])
            self.VEHICLES[ve].load += self.REQUESTS[self.request_selected[re]].count
            self.REQUESTS[self.request_selected[re]].served = 1
            self.VEHICLES[ve].update_route()
        self.request_selected = []
        self.vehicle = []
        self.time += 1
        step_time = 0 if self.time == 1440 else self.time
        for ve in self.vehicle:
            self.VEHICLES[ve].step(step_time)
        if self.time == 1440:
            done = True
            return [], [], done
        for grid in self.request_all[self.day][self.time].keys():
            self.request_selected += self.request_all[self.day][self.time][grid]
        if self.day > 1 and self.time < 20:
            # for grid in self.request_all[self.day-1].keys():
            for time in range(1440 + self.time - 20, 1440):
                for grid in self.request_all[self.day - 1][time].keys():
                    self.request_selected += self.request_all[self.day - 1][time][grid]
        else:
            # for grid in self.request_all[self.day].keys():
            for time in range(self.time - 20, self.time):
                for grid in self.request_all[self.day][time].keys():
                    self.request_selected += self.request_all[self.day][time][grid]
        if len(self.request_selected) > REQUEST_NUMS:
            random.seed(10)
            self.request_selected = random.sample(self.request_selected, REQUEST_NUMS)
        else:
            self.request_selected += [-1] * (REQUEST_NUMS - len(self.request_selected))
        '''
            select N vehicles, vehicle_state consider the next grid the car going to ???
        '''
        for i in range(len(self.VEHICLES)):
            if (self.VEHICLES[i].stop_time < self.VEHICLES[i].start_time and self.VEHICLES[i].stop_time >= self.time) \
                    or (self.VEHICLES[i].start_time < self.VEHICLES[i].stop_time and (
                    self.VEHICLES[i].start_time <= self.time and self.VEHICLES[i].stop_time >= self.time)):
                if self.VEHICLES[i].load < self.VEHICLES[i].cap:
                    self.VEHICLES[i].serving = 1
                    self.vehicle.append(i)
        done = False if self.time < 1440 else True
        return self.request_selected, self.vehicle, done

    def reset(self, day):
        self.day = day
        self.time = 0
        self.request_selected = []
        self.vehicle = []
        '''
            select M requests
        '''
        for grid in self.request_all[day][0].keys():
            self.request_selected += self.request_all[day][0][grid]
        if self.day > 1:
            # for grid in self.request_all[day-1].keys():
            for time in range(1420, 1440):
                for grid in self.request_all[day - 1][time].keys():
                    self.request_selected += self.request_all[day - 1][time][grid]
        if len(self.request_selected) > REQUEST_NUMS:
            random.seed(10)
            self.request_selected = random.sample(self.request_selected, REQUEST_NUMS)
        else:
            self.request_selected += [-1] * (REQUEST_NUMS - len(self.request_selected))
        '''
            select N vehicles, vehicle_state consider the next grid the car going to ???
        '''
        for i in range(len(self.VEHICLES)):
            if self.VEHICLES[i].stop_time < self.VEHICLES[i].start_time or self.VEHICLES[i].start_time == 0:
                if self.VEHICLES[i].load < self.VEHICLES[i].cap:
                    self.VEHICLES[i].serving = 1
                    self.vehicle.append(i)
        return self.request_selected, self.vehicle
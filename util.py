#!/usr/bin/env python
# -*- coding: utf-8 -*-

from floyd_path import plan_route
from global_parameters import get_value
import copy
class Request(object):
    def __init__(self, r_id, day: int, origin: int, destination: int, time: int, count: int):
        self.r_id = r_id
        self.day = day
        self.origin = origin
        self.destination = destination
        self.count = count
        self.served = 0
        self.pu_t = 0
        self.appear_time = time

class Vehicle(object):
    def __init__(self, v_id, location: int, start_time: int, stop_time: int):
        self.v_id = v_id
        self.location = location
        self.loc_time = 0
        self.start_time = start_time
        self.stop_time = stop_time
        self.cap = 4
        self.load = 0
        self.serving = 0
        self.pick_up = []
        self.onboard = []
        self.re_to_pick = []
        self.route = []
        self.passed_route = []
        self.violation_time = 0
        self.drop_off_slot = []

    def step(self, current_time):
        drive_time = 1440 if current_time == 0 else 0
        if (self.stop_time < self.start_time and self.stop_time < current_time) \
                or (self.stop_time > self.start_time and (current_time < self.start_time or current_time > self.stop_time)):
            self.serving = 0
        current_hour = int(current_time / 60)
        travel_time = get_value('travel_time')
        t_time = travel_time[current_hour][self.location][self.route[0]]
        if travel_time[current_hour][self.location][self.route[0]] == 0:
            t_hour = current_hour - 1 if current_hour > 0 else 23
            t_time = travel_time[t_hour][self.location][self.route[0]]
        if drive_time - self.loc_time >= t_time:
            self.location = self.route[0]
            self.route.pop(0)
        REQUESTS = get_value('REQUESTS')
        temp_onboard = copy.copy(self.onboard)
        for re in temp_onboard:
            if REQUESTS[re].destination == self.location:
                self.onboard.remove(re)
                self.load -= REQUESTS[re].count
        temp_re_to_pick = copy.copy(self.re_to_pick)
        for re in temp_re_to_pick:
            if REQUESTS[re].origin == self.location:
                self.onboard.append(re)
                REQUESTS[re].pu_t = current_time
                self.re_to_pick.remove(re)
                self.load += REQUESTS[re].count

    def update_route(self):
        self.re_to_pick = list(set(self.pick_up) ^ set(self.onboard))
        isEmpty = True if len(self.onboard) == 0 else False
        self.route = plan_route(self.location, self.re_to_pick, isEmpty, self.onboard)



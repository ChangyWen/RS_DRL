#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Request(object):
    def __init__(self, r_id, day: int, origin: int, destination: int, time: int, count: int):
        self.r_id = r_id
        self.origin = origin
        self.destination = destination
        self.count = count
        self.served = 0
        self.pu_t = 0
        self.delay_t = 0
        self.appear_slot = time

class Vehicle(object):
    def __init__(self, v_id, location: int, start_time: int, stop_time: int):
        self.v_id = v_id
        self.location = location
        self.start_time = start_time
        self.stop_time = stop_time
        self.cap = 4
        self.load = 0
        self.serving = 0

        self.picked_up = []
        self.route = []
        self.passed_route = []
        self.violation_time = 0
        self.drop_off_slot = []


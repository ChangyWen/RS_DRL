#!/usr/bin/env python
# -*- coding: utf-8 -*-

import networkx as nx
from global_parameters import get_value
from collections import OrderedDict
def floyd_warshall(distance):
    '''
    :param distance: distance model with maxsize
    :return: shortest_dis, predecessors
    '''
    G = nx.DiGraph(distance)
    shortest_dis = nx.floyd_warshall(G)
    predecessors, _ = nx.floyd_warshall_predecessor_and_distance(G)
    return shortest_dis, predecessors

def get_route(source, target):
    predecessors = get_value('predecessors')
    route = nx.reconstruct_path(source, target, predecessors)
    return route

def get_distance(source, target):
    shortest_dis = get_value('shortest_dis')
    return shortest_dis[source][target]

def plan_route(loc, re_to_pick, isEmpty, onboard):
    REQUESTS = get_value('REQUESTS')
    origin = []
    destination = []
    if len(re_to_pick) == 1:
        re = re_to_pick[0]
        origin = REQUESTS[re].origin
        if isEmpty:
            destination = REQUESTS[re].destination
            return_route = []
            return_route += get_route(loc, origin)
            return_route.pop(-1)
            return_route += get_route(origin, destination)
            return return_route.pop(0)
        else:
            destination.append(REQUESTS[onboard[0]].destination)
            destination.append(REQUESTS[re].destination)
            route_all = [[origin, destination[0], destination[1]],
                         [origin, destination[1], destination[0]]]
            s = loc
            dis_all = {}
            for i in range(len(route_all)):
                route = route_all[i]
                dis = 0
                for grid in route:
                    dis += get_distance(s, grid)
                    s = grid
                dis_all[i] = dis
            dis_all_sorted = OrderedDict(sorted(dis_all.items(), key=lambda t: t[1]))
            key = list(dis_all_sorted.keys())[0]
            temp_route = route_all[key]
            return_route = []
            return_route += get_route(loc, temp_route[0])
            return_route.pop(-1)
            return_route += get_route(temp_route[0], temp_route[1])
            return_route.pop(-1)
            return_route += get_route(temp_route[1], temp_route[2])
            return return_route.pop(0)
    if len(re_to_pick) > 1:
        for re in re_to_pick:
            origin.append(REQUESTS[re].origin)
            destination.append(REQUESTS[re].destination)
        route_all = [[origin[0], origin[1], destination[0], destination[1]],
                     [origin[1], origin[0], destination[1], destination[0]],
                     [origin[0], origin[1], destination[1], destination[0]],
                     [origin[1], origin[0], destination[0], destination[1]]]
        s = loc
        dis_all = {}
        for i in range(len(route_all)):
            route = route_all[i]
            dis = 0
            for grid in route:
                dis += get_distance(s, grid)
                s = grid
            dis_all[i] = dis
        dis_all_sorted = OrderedDict(sorted(dis_all.items(),key=lambda t:t[1]))
        key = list(dis_all_sorted.keys())[0]
        temp_route = route_all[key]
        return_route = []
        return_route += get_route(loc, temp_route[0])
        return_route.pop(-1)
        return_route += get_route(temp_route[0], temp_route[1])
        return_route.pop(-1)
        return_route += get_route(temp_route[1], temp_route[2])
        return_route.pop(-1)
        return_route += get_route(temp_route[2], temp_route[3])
        return  return_route.pop(0)




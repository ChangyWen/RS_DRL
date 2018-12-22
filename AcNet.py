#!/usr/bin/env python
# -*- coding: utf-8 -*-


class AcNet(object):
    '''
    Class: A3C network
    '''
    def __init__(self, a_dim, s_dim,):
        '''
        :param a_dim: The dimension of the action
        :param s_dim: The dimension of the state
        '''
        pass

    def _build_net(self, scope):
        '''
        :param scope: The network it belongs to
        :return:
        '''
        pass

    def choose_action(self, s):
        '''
        :param s: state
        :return:
        '''
        pass

    def pull_global(self):
        '''
        Pull operation: Pull the up-to-date parameters to the local_net from the global_net
        '''
        pass

    def update_global(self):
        '''
        Push operation: Push the up-to-date parameters to the global_net from the local_net
                        Run by a local_net
        '''
        pass



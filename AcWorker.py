#!/usr/bin/env python
# -*- coding: utf-8 -*-

from global_parameters import *
from rs_env import RideSharing_Env
from AcNet import AcNet
from hyper_parameters import *

class Worker(object):
    '''
    Class: Worker of AcNet work [job: def work()] in parallel
    '''
    def __init__(self, name, globalAC):
        '''
        :param name: worker's name
        :param globalAC: worker's global_net's name
        '''
        self.env = RideSharing_Env() ### initialize the rs env
        self.name = name
        self.AC = AcNet(scope=name, globalAC=globalAC)

    def work(self):
        '''
        The job of the the Workers
        '''
        SESS = get_value('SESS')
        # GLOBAL_RUNNING_R = get_value('GlOBAL_RUNNING_R')
        GLOBAL_EP = get_value('GLOBAL_EP')
        COORD = get_value('COORD')
        total_step = 1  ### local_net step counter
        buffer_s, buffer_a, buffer_r = [], [], []
        day = 1
        while not COORD.should_stop() and GLOBAL_EP < MAX_GLOBAL_EP:
            GLOBAL_RUNNING_R = get_value('GlOBAL_RUNNING_R')
            GLOBAL_EP = get_value('GLOBAL_EP')
            s = self.env.reset(day)
            day += 1
            ep_r = 0 ### episode reward in local_net
            for ep_t in range(MAX_EP_STEP):
                a_temp = self.AC.choose_action(s)
                a, s_, r, done, info = self.env.step(a_temp)
                done = True if ep_t == MAX_EP_STEP - 1 else False
                ep_r += r
                buffer_s.append(s)
                buffer_a.append(a)
                buffer_r.append(r)
                if total_step % UPDATE_GLOBAL_ITER == 0 or done:
                    if done:
                        v_s_ = 0 ### termial state
                    else:
                        v_s_ = SESS.run(self.AC.v,
                                        feed_dict={self.AC.s: s_[np.newaxis, :]})
                    buffer_v_target = []
                    for r in buffer_r[::-1]:
                        v_s_ = r + GAMMA * v_s_
                        buffer_v_target.append(v_s_)
                    buffer_v_target.reverse()
                    buffer_s, buffer_a, buffer_v_target = \
                        np.vstack(buffer_s), np.vstack(buffer_a), np.vstack(buffer_v_target)
                    feed_dict = {self.AC.s: buffer_s,
                                 self.AC.a_his: buffer_a,
                                 self.AC.v_target: buffer_v_target}
                    print('worker_name:',self.name, 'update')
                    self.AC.update_global(feed_dict)
                    buffer_s, buffer_a, buffer_r = [], [], []
                    self.AC.pull_global()
                s = s_
                total_step += 1
                if done:
                    ### Exponentially weighted average over UPDATE_GLOBAL_ITER steps ###
                    if len(GLOBAL_RUNNING_R) == 0:
                        GLOBAL_RUNNING_R.append(ep_r)
                    else:
                        GLOBAL_RUNNING_R.append(EWA_BETA * GLOBAL_RUNNING_R[-1] + (1 - EWA_BETA) * ep_r)
                        print(self.name, 'Ep:', GLOBAL_EP, '| Ep_r: %i' % GLOBAL_RUNNING_R[-1])
                    GLOBAL_EP += 1
                    set_value('GLOBAL_EP', GLOBAL_EP)
                    set_value('GLOBAL_RUNNING_R', GLOBAL_RUNNING_R)
                    break
#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
using
tensorflow 1.12.0
python 3.6.7

Project: Ride-sharing with deep reinforcement learning (A3C)
'''
__author__ = 'SRIBD_Ride-sharing'

from AcWorker import *
from hyper_parameters import *
import os
import shutil
import threading
import matplotlib.pyplot as plt

if __name__ == "__main__":
    with tf.device("/cpu:0"):
        set_value('OPT_A', tf.train.RMSPropOptimizer(LR_A, name='RMSProp_A'))
        set_value('OPT_C', tf.train.RMSPropOptimizer(LR_C, name='RMSProp_C'))
        global_AC = AcNet(GLOBAL_NET_SCOPE)
        workers = []
        for i in range(N_WORKERS):
            i_name = 'w_%i' % i
            workers.append(Worker(i_name, global_AC))

    saver = tf.train.Saver()
    set_value('SESS', tf.Session())
    set_value('COORD', tf.train.Coordinator())
    COORD = get_value('COORD')
    SESS = get_value('SESS')
    SESS.run(tf.global_variables_initializer())

    if OUTPUT_GRAPH:
        if os.path.exists(LOG_DIR):
            shutil.rmtree(LOG_DIR)
        tf.summary.FileWriter(LOG_DIR, SESS.graph)

    worker_threads = []
    for worker in workers:
        job = lambda: worker.work()
        t = threading.Thread(target=job)
        t.start()
        worker_threads.append(t)
    COORD.join(worker_threads)

    save_path = saver.save(SESS, 'net_param/net_param.ckpt')

    SESS.close()
    '''Plot to check the total moving reward'''
    GLOBAL_RUNNING_R = get_value('GLOBAL_RUNNING_R')
    plt.plot(np.arange(len(GLOBAL_RUNNING_R)), GLOBAL_RUNNING_R)
    plt.xlabel('Step')
    plt.ylabel('Total moving reward')
    plt.show()
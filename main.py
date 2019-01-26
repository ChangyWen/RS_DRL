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
from read_data import read_request_data
import os
import shutil
import threading
import matplotlib.pyplot as plt
import initial

if __name__ == "__main__":
    set_value('SESS', tf.Session())
    DATA = read_request_data('trip_data/filtered_yellow_tripdata_2018-06.csv')
    isTrain = True
    print(N_WORKERS)
    set_value('DATA', DATA)
    print('point1: initialize begin')
    request_all = initial.initialize()
    print('point2: initialize end')
    set_value('request_all', request_all)
    with tf.device("/cpu:0"):
        set_value('OPT_A', tf.train.RMSPropOptimizer(LR_A, name='RMSProp_A'))
        set_value('OPT_C', tf.train.RMSPropOptimizer(LR_C, name='RMSProp_C'))
        global_AC = AcNet(GLOBAL_NET_SCOPE)
        workers = []
        for i in range(N_WORKERS):
            print('%i worker:' % i)
            i_name = 'w_%i' % i
            workers.append(Worker(i_name, global_AC))

    set_value('COORD', tf.train.Coordinator())
    COORD = get_value('COORD')
    SESS = get_value('SESS')
    SESS.run(tf.global_variables_initializer())
    saver = tf.train.Saver(max_to_keep=1)

    if isTrain:
        if OUTPUT_GRAPH:
            if os.path.exists(LOG_DIR):
                shutil.rmtree(LOG_DIR)
            tf.summary.FileWriter(LOG_DIR, SESS.graph)

        worker_threads = []
        i = 1
        for worker in workers:
            job = lambda: worker.work()
            t = threading.Thread(target=job)
            print('worker %i appended...' % i)
            i += 1
            t.start()
            worker_threads.append(t)
        print('all worker begin')
        COORD.join(worker_threads)
        save_path = saver.save(SESS, 'net_model/net_model_01.ckpt')
    else:
        model_file = tf.train.latest_checkpoint('net_model/')
        saver.restore(SESS, model_file)
    SESS.close()
    '''Plot to check the total moving reward'''
    GLOBAL_RUNNING_R = get_value('GLOBAL_RUNNING_R')
    plt.plot(np.arange(len(GLOBAL_RUNNING_R)), GLOBAL_RUNNING_R)
    plt.xlabel('Step')
    plt.ylabel('Total moving reward')
    plt.savefig('./ver_01.pdf')
    # plt.show()
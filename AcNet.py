#!/usr/bin/env python
# -*- coding: utf-8 -*-
from hyper_parameters import *
from global_parameters import *

class AcNet(object):
    '''
    Class: A3C network
    '''
    def __init__(self, scope, globalAC=None):
        '''
        :param scope: The network it belongs to
        :param globalAC: The global_net name
        '''
        self.SESS = get_value('SESS')
        self.OPT_A = get_value('OPT_A')
        self.OPT_C = get_value('OPT_C')

        if scope == GLOBAL_NET_SCOPE:
            '''Global_net initialization'''
            with tf.variable_scope(scope):
                self.s = tf.placeholder(dtype=tf.float32, shape=[None, N_S], name='S')
                self.a_params, self.c_params = self._build_net(scope)[-2:]   ### the last 2 return of build_net function
        else:
            with tf.variable_scope(scope):
                self.s = tf.placeholder(dtype=tf.float32, shape=[None, N_S], name='S')
                self.a_his = tf.placeholder(dtype=tf.int32, shape=[None, N_A], name='A')
                self.v_target = tf.placeholder(dtype=tf.float32, shape=[None, 1], name='Vtarget')
                self.a_prob, self.v, self.a_params, self.c_params = self._build_net(scope)
                td = tf.subtract(self.v_target, self.v, name='TD_Error')

                with tf.name_scope('c_loss'):
                    self.c_loss = tf.reduce_mean(tf.square(td))

                with tf.name_scope('a_loss'):
                    log_prob = tf.reduce_sum(
                        tf.log(self.a_prob + 1e-5) * tf.one_hot(indices=self.a_his, depth=N_A, dtype=tf.float32),
                        axis=1,
                        keep_dims=True)
                    exp_v = log_prob * tf.stop_gradient(td)
                    entropy = -tf.reduce_sum(self.a_prob * tf.log(self.a_prob + 1e-5),
                                             axis=1,
                                             keep_dims=True)
                    self.exp_v = exp_v + ENTROPY_BETA * entropy
                    self.a_loss = tf.reduce_mean(-self.exp_v)

                with tf.name_scope('local_grad'):
                    self.a_grads = tf.gradients(self.a_loss, self.a_params)
                    self.c_grads = tf.gradients(self.c_loss, self.c_params)

            with tf.name_scope('sync'):
                with tf.name_scope('pull'):
                    self.pull_a_params = [l_p.assign(g_p) for l_p, g_p in zip(self.a_params, globalAC.a_params)]
                    self.pull_c_params = [l_p.assign(g_p) for l_p, g_p in zip(self.c_params, globalAC.c_params)]
                with tf.name_scope('push'):
                    self.push_a_params = self.OPT_A.apply_gradients(zip(self.a_grads, globalAC.a_params))
                    self.push_c_params = self.OPT_C.apply_gradients(zip(self.c_grads, globalAC.c_params))

    def _build_net(self, scope):
        '''
        :param scope: The network it belongs to
        :return: a_prob (M * N), v, a_params, c_params
        '''
        with tf.variable_scope('actor'):
            ### Variable
            # W_a1 = tf.Variable(tf.truncated_normal([N_S, UNIT_A], stddev=0.5), dtype=tf.float32, name='W_a1')
            # b_a1 = tf.Variable(tf.zeros([UNIT_A]), dtype=tf.float32, name='b_a1')
            # W_a2 = tf.Variable(tf.truncated_normal([UNIT_A, UNIT_A], stddev=0.5), dtype=tf.float32, name='W_a2')
            # b_a2 = tf.Variable(tf.zeros([UNIT_A]), dtype=tf.float32, name='b_a2')
            # W_prob = tf.Variable(tf.truncated_normal([UNIT_A, N_A], stddev=0.5), dtype=tf.float32, name='W_prob')
            # b_prob = tf.Variable(tf.zeros([N_A]), dtype=tf.float32, name='b_prob')
            # activation = tf.nn.relu(tf.nn.bias_add(tf.matmul(self.s, W_a1),b_a1))
            layer_a1 = tf.layers.dense(inputs = self.s,
                                  units = UNIT_A,
                                  activation = tf.nn.relu6,
                                  kernel_initializer = W_INIT,
                                  name = 'layer_a1')
            layer_a2 = tf.layers.dense(inputs = layer_a1,
                                       units = UNIT_A,
                                       activation = tf.nn.relu6,
                                       kernel_initializer = W_INIT,
                                       name = 'layer_a2')
            a_prob = tf.layers.dense(inputs=layer_a2,
                                     units=N_A,   ### N_A = M*N
                                     activation=tf.nn.tanh,
                                     kernel_initializer=W_INIT,
                                     name = 'a_prob')
        with tf.variable_scope('critic'):
            # W_c1 = tf.Variable(tf.truncated_normal([N_S, UNIT_C], stddev=0.2), dtype=tf.float32, name='W_c1')
            # b_c1 = tf.Variable(tf.zeros([UNIT_A]), dtype=tf.float32, name='b_c1')
            # W_c2 = tf.Variable(tf.truncated_normal([UNIT_C, UNIT_C], stddev=0.2), dtype=tf.float32, name='W_c2')
            # b_c2 = tf.Variable(tf.zeros([UNIT_A]), dtype=tf.float32, name='b_c2')
            # W_v = tf.Variable(tf.truncated_normal([UNIT_C, 1], stddev=0.2), dtype=tf.float32, name='W_v')
            # b_v = tf.Variable(tf.zeros([1]), dtype=tf.float32, name='b_v')
            layer_c1 = tf.layers.dense(inputs = self.s,
                                       units = UNIT_C,
                                       activation = tf.nn.relu6,
                                       kernel_initializer = W_INIT,
                                       name = 'layer_c1')
            layer_c2 = tf.layers.dense(inputs = layer_c1,
                                       units = UNIT_C,
                                       activation = tf.nn.relu6,
                                       kernel_initializer = W_INIT,
                                       name = 'layer_c2')
            v = tf.layers.dense(inputs = layer_c2,
                                units = 1,
                                kernel_initializer = W_INIT,
                                name = 'v')
        a_params = tf.get_collection(key=tf.GraphKeys.TRAINABLE_VARIABLES, scope=scope + '/actor')
        c_params = tf.get_collection(key=tf.GraphKeys.TRAINABLE_VARIABLES, scope=scope + '/critic')
        return a_prob, v, a_params, c_params

    def choose_action(self, s): ## ?
        '''
        :param s: state
        :return: action
        '''
        action = self.SESS.run(self.a_prob, feed_dict={self.s: s[np.newaxis, :]})
        return action

    def pull_global(self):
        '''
        Pull operation: Pull the up-to-date parameters to the local_net from the global_net
        '''
        self.SESS.run([self.pull_a_params, self.pull_c_params])

    def update_global(self, feed_dict):
        '''
        Push operation: Push the up-to-date parameters to the global_net from the local_net
                        Run by a local_net
        :param feed_dict: feed_dict
        '''
        self.SESS.run([self.push_a_params, self.push_c_params], feed_dict)




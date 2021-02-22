# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 17:00:49 2020

@author: sgyhi
"""

from abc import ABCMeta, abstractmethod
import random
import numpy as np
import operator
import networkx as nx
import copy
from gamestate import GameState
import sys
import random
from itertools import product


class Policy(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def move(self, state):
        pass


class DefaultPolicy(Policy):
    def move(self, state):
        """Chooses moves from the legal moves in a given state"""
        # print(state.legal_moves(state.currNode))
        if not state.legal_moves():
            return {}
        actions = {}
        for robot in state.legal_moves():
            actions[robot] = random.sample(state.legal_moves()[robot], 1)[0]
        return actions


class MCTSPolicy_basic(Policy):
    """
    Implementation of Monte Carlo Tree Search
    """

    def __init__(self, root_state):
        self.digraph = nx.DiGraph()
        self.EPSILON = 10e-6  # Prevents division by 0 in calculation of UCT

        # Constant parameter to weight exploration vs. exploitation for UCT
        # check other implementations for reward instead of win/lose case
        # https://github.com/GuangyaoSHI/mcts/blob/master/include/mcts/defaults.hpp
        self.uct_c = np.sqrt(2)

        self.node_counter = 0
        self.digraph.add_node(self.node_counter,
                              reward=0,
                              n=0,
                              uct=sys.maxsize,
                              state=root_state)
        self.node_counter += 1

    def is_leaf_node(self, node):
        if (self.digraph.in_degree(node) == 0) \
                and (self.digraph.out_degree(node) == 0):
            return True
        elif (self.digraph.in_degree(node) == 1) \
                and (self.digraph.out_degree(node) == 0):
            return True
        else:
            return False

    def selection(self, root):
        """
        Starting at root, recursively select the best node that maximizes UCT
        until a node is reached that has no explored children
        Keeps track of the path traversed by adding each node to path as
        it is visited
        :return: the node to expand
        """

        # if the search tree is empty, initialize it with root
        # if not list(self.digraph.nodes()):
        #     self.digraph.add_node(self.node_counter, \
        #                           attr_dict={'reward':0,\
        #                                      'n':0, \
        #                                      'uct':sys.maxsize,\
        #                                      'state':root})
        #     self.node_counter += 1
        #     return root

        if self.is_leaf_node(root):
            return root
        else:
            # the current node is not a leaf node
            # print('root is not a leaf node')
            # handle the general case
            children = self.digraph.successors(root)
            uct_values = {}
            for child_node in children:
                uct_values[child_node] = self.uct(node=child_node, parent=root)

            # Choose the child node that maximizes the expected value given by UCT
            best_child_node = max(uct_values.items(), key=operator.itemgetter(1))[0]

            return self.selection(best_child_node)

    def expansion(self, node):
        # if n == 0, just rollout
        # if n >0, expand all children and select one to rollout
        if self.digraph.nodes[node]['n'] == 0:
            return node
        else:
            curr_game_pos = self.digraph.nodes[node]['state'].currNode
            legal_moves = self.digraph.nodes[node]['state'].legal_moves()
            # print('Legal moves: {}'.format(legal_moves))
            # if node is a terminal state, e.g. run out of budget
            # legal_moves will be empty
            if not legal_moves:
                return node
        # for each available action from the current state, add all new states
        # to the tree
        child_node_id = []
        # legal_moves = {robot:[actions]}
        # Todo: if some robots have empty set, the following code
        # will return empty set on joint_moves
        # !!!!!this is a problem!!!!
        joint_actions = list(product(*list(legal_moves.values())))
        # check whether the joint action set is empty
        assert joint_actions, 'joint action set is empty'
        joint_moves = [dict(zip(list(legal_moves.keys()), joint_action)) \
                       for joint_action in joint_actions]
        for move in joint_moves:
            # print('adding to expansion analysis with: {}'.format(move))
            child = self.digraph.nodes[node]['state'].transition_function(move)
            self.digraph.add_node(self.node_counter,
                                  reward=0,
                                  n=0,
                                  uct=sys.maxsize,
                                  state=child)
            self.digraph.add_edge(node, self.node_counter, action=move)
            child_node_id.append(self.node_counter)
            self.node_counter += 1
        # return first new child
        # Todo: uniform sampling

        return child_node_id[0]

    def simulation(self, node):
        """
        Conducts a light playout from the specified node
        :return: The reward obtained once a terminal state is reached
        """
        # reward should be defined
        """
        Conducts a light playout from the specified node
        :return: The reward obtained once a terminal state is reached
        """
        random_policy = DefaultPolicy()
        # current world state
        current_state = self.digraph.nodes[node]['state']
        while not current_state.is_terminal():
            # move is a list with one element or empty
            move = random_policy.move(current_state)
            if not move:
                break
            current_state = current_state.transition_function(move)
        return current_state.collected_reward()

    def backpropagation(self, last_visited, reward):
        '''
        Walk the path upwards to the root, incrementing the 'n' 
        and 'reward' attributes of the nodes along the way
        '''
        current = last_visited
        while True:
            self.digraph.nodes[current]['n'] += 1
            self.digraph.nodes[current]['reward'] += reward

            # carefully check the following statement
            # Todo
            if not list(self.digraph.predecessors(current)):
                break
            else:
                try:
                    # Todo
                    current = list(self.digraph.predecessors(current))[0]
                except IndexError:
                    break

    def uct(self, node, parent):
        """
        Returns the expected value of a state, calculated as a weighted sum of
        its exploitation value and exploration value
        """
        n = self.digraph.nodes[node]['n']  # Number of plays from this node
        # total reward generated passing through this node
        # keep track of average is better
        reward = self.digraph.nodes[node]['reward']
        # number of times the parent node has been visited
        N = self.digraph.nodes[parent]['n']
        c = self.uct_c
        epsilon = self.EPSILON

        exploitation_value = reward / (n + epsilon)
        exploration_value = 2.0 * c * np.sqrt(2 * np.log(N) / (n + epsilon))

        value = exploitation_value + exploration_value

        self.digraph.nodes[node]['uct'] = value

        return value

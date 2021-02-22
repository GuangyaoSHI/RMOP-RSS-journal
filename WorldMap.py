# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 12:04:42 2020

@author: sgyhi
"""

"""
Multi-robot Orienteering Problem as a tree search
<state representation, transition function, move function, \
    terminal detector>
"""
import networkx as nx
import copy


class WorldMap():
    def __init__(self, graph, start, horizon):
        self.G = graph
        self.horizon = horizon
        # starts is a dictionary of starting positions of robots
        # starts = {robot:position}
        self.currNode = start
        # attri corresponds to 'visited' property of each node
        attri = {}
        self.paths_robots = {}
        self.attack_indicator = {}
        for node in self.G.nodes:
            attri[node] = []
        for robot in start:
            self.paths_robots[robot] = [start[robot]]
            attri[start[robot]].append(robot)
            self.attack_indicator[robot] = 0
        nx.set_node_attributes(self.G, attri, 'visited')




    def move(self, next_node):
        # next_node is a dictionary
        # {robot:next_position}
        for robot in next_node:
            next_pos = next_node[robot]
            self.paths_robots[robot].append(next_pos)
            self.G.nodes[next_pos]['visited'].append(robot)
        self.horizon -= 1
        self.currNode = next_node

    def legal_moves(self):
        """
        return the neighbors of the current node
        in the form {robot:[neighbors]}
        if the robot has run out of budget, return an empty dict
        attack_indicator = {robot:indicator}
        """
        possible_moves = {}
        # check if budget has been used up
        if self.horizon <= 0:
            # print('Time up!')
            return possible_moves
        for robot in self.currNode:
            curr_pos = self.currNode[robot]
            if self.attack_indicator[robot]:
                # if the robot is already attacked, stay in the same position
                possible_moves[robot] = [curr_pos]
            else:
                possible_moves[robot] = list(self.G.neighbors(curr_pos))
        return possible_moves

    def transition_function(self, next_node):
        # verify that the next position is legal
        for robot in next_node:
            assert next_node[robot] in self.legal_moves()[robot]
        # First, make a copy of the current state
        new_state = copy.deepcopy(self)

        # Then, apply the action to produce the new state
        new_state.move(next_node)

        return new_state

    def is_terminal(self):
        if self.horizon > 0:
            return False
        else:
            return True

    def collected_reward(self):
        # compute the reward associated with the current state
        total = 0
        for node in self.G.nodes:
            if self.G.nodes[node]['visited']:
                total += self.G.nodes[node]['reward']
        return total


def test(starts=[(0, 0), (4, 0)]):
    gamestate = WorldMap(starts)
    legal_moves = gamestate.legal_moves(starts)
    gamestate.move((1, 0))
    pos = {}
    labels = {}
    for node in gamestate.G.nodes:
        pos[node] = node
        labels[node] = gamestate.G.nodes[node]['reward']
    nx.draw(gamestate.G, pos=pos, with_labels=True)

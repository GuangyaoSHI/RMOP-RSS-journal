# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 12:04:42 2020

@author: sgyhi
"""

"""
Multi-robot Orienteering Problem as a game
<state representation, transition function, move function, \
    terminal detector>
"""
import networkx as nx
import copy

class GameState_no_attack:
    def __init__(self, G, starts):
        self.G = G
        self.horizon = 4
        #starts is a dictionary of starting positions of robots
        #starts = {robot:position}
        self.currNode = starts
        #attri corresponds to 'visited' property of each node
        attri = {}
        for node in self.G.nodes:
            attri[node] = []
        for robot in starts:
            attri[starts[robot]].append(robot) 
        nx.set_node_attributes(self.G, attri, 'visited')

    # GameState needs to be hashable so that it can be used as a unique graph
    # node in NetworkX
    def __key(self):
        return self.__str__()

    def __eq__(x, y):
        return x.__key() == y.__key()

    def __hash__(self):
        return hash(self.__key())
    
    def __str__(self):
        output = ''
        for h in range(self.grid_height):
            for l in range(self.grid_len):
                contents = self.G.nodes[(l, self.grid_height-1-h)]['visited']
                if l < self.grid_len-1:
                    output += '{}'.format(contents)
                else:
                    output += '{}\n'.format(contents)
        #somthing like
        #  '[] [] [1,2]
        #   [] [2,3] []'                                                                                                            
        return output
    
    def move(self, next_node):
        #next_node is a dictionary 
        #{robot:next_position}
        for robot in next_node:
            next_pos = next_node[robot]
            self.G.nodes[next_pos]['visited'].append(robot)
        self.horizon -= 1
        self.currNode = next_node
        
    def legal_moves(self, currNode):
        """
        return the neighbors of the current node
        in the form {robot:[neighbors]}
        if the robot has run out of budget, return an empty dict
        """
        possible_moves = {}
        #check if budget has been used up
        if self.horizon <= 0:
            #print('Time up!')
            return possible_moves
        for robot in currNode:
            curr_pos = currNode[robot]
            possible_moves[robot] = list(self.G.neighbors(curr_pos))
        return possible_moves
    
    def transition_function(self, next_node):
        #verify that the next position is legal
        for robot in next_node:
            assert next_node[robot] in self.legal_moves(self.currNode)[robot]
        #First, make a copy of the current state
        new_state = copy.deepcopy(self)
        
        #Then, apply the action to produce the new state
        new_state.move(next_node)
        
        return new_state
    
    def is_terminal(self):
        if self.horizon > 0:
            return False
        else:
            return True
        
    def collected_reward(self):
        #compute the reward associated with the current state
        total = 0
        for node in self.G.nodes:
            if self.G.nodes[node]['visited']:
                total += self.G.nodes[node]['reward']
        return total
        
def test(starts=[(0,0),(4,0)]):
    gamestate = GameState(starts)
    print(gamestate.__str__())
    legal_moves = gamestate.legal_moves(starts)
    gamestate.move((1,0))
    print(gamestate.__str__())
    pos = {}
    labels = {}
    for node in gamestate.G.nodes:
        pos[node] = node
        labels[node] = gamestate.G.nodes[node]['reward']
    nx.draw(gamestate.G, pos=pos, with_labels = True)
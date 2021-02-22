from WorldMap import *
from policies_no_attack import *
import networkx as nx
from play_game import *
from gamestate import *


def naive_planning(budget, start, board, horizon, alpha, attacker_policy):
    pos_init = {}
    for robot in start:
        pos_init[robot] = start[robot][0]
    # robot use world map to do planning
    world_map = WorldMap(board, pos_init, horizon)
    # attackers use game state to do planning
    game = GameState(board, start, 'attacker', horizon, alpha)
    # record all paths
    # starting position
    pos_init = {}
    for robot in start:
        pos_init[robot] = start[robot][0]
    path = [pos_init]

    while not game.is_terminal():
        # attackers first do the tree search
        next_node, mcts = mcts_process(game, budget)
        # then move
        game.move(next_node)

        # robot start to do planning
        # first find attack indicator
        attack_indicator = {}
        for robot in next_node:
            attack_indicator[robot] = next_node[robot][1]
        world_map.attack_indicator = attack_indicator
        mcts = MCTSPolicy_basic(world_map)
        for j in range(budget):
            node_exp = mcts.selection(0)
            node_fron = mcts.expansion(node_exp)
            reward = mcts.simulation(node_fron)
            mcts.backpropagation(node_fron, reward)
        # select one action based on average reward
        actions = {}
        for node in mcts.digraph.successors(0):
            reward = mcts.digraph.nodes[node]['reward'] / mcts.digraph.nodes[node]['n']
            actions[reward] = \
                mcts.digraph.edges[0, node]['action']
        next_node = actions[max(actions)]
        path.append(next_node)
        world_map.move(next_node)
        # also need to move in the game state
        next_in_game = {}
        for robot in next_node:
            next_in_game[robot] = [next_node[robot], attack_indicator[robot]]
        game.move(next_in_game)

    # print('collected reward with MCTS basic: {}'.format(world_map.collected_reward()))
    # print('robot paths: {}'.format(world_map.paths_robots))
    return world_map, game

if __name__ == "__main__":
    budget = 600
    start = {0: [(0, 1), 0], 1: [(5, 1), 0], 2: [(6, 6), 0], 3: [(10, 10), 0]}
    graph = generate_grid_map(15, 15, 1)
    horizon = 6
    alpha = 2
    robot_policy = 'random'
    attacker_policy = 'mcts'
    world_map, game = naive_planning(budget, start, graph, horizon, alpha, attacker_policy)
    print('reward is (from game state) {}'.format(game.collected_reward()))

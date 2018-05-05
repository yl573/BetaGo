
from MCTS import MCTS
from Shared.Functions import toggle_player
from GoGame.GoSimulator import GoSimulator
import numpy as np
import random


# class Agent:


class MCTSAgent:
    def __init__(self, model, player, size, input_moves, start_boards):
        self.mcts = MCTS(model, player, size, input_moves, start_boards=start_boards)

    def select_move(self, boards, player):
        pi = self.mcts.search_for_pi(iterations=iters)
        # Find position of next play that maximises pi
        move = np.random.choice(len(pi), p=pi)
        self.mcts.set_move(move)
        return move, pi

class RandomAgent:

    def __init__(self):
        pass
        
    def select_move(self, boards, player):
        n = boards.shape[1]
        game = GoSimulator(n)
        game.set_board_from_prev_boards(boards, player) 
        legal = game.get_legal_moves().flatten()
        pi = np.append(legal,[1])
        pi = np.divide(pi, np.sum(pi))
        move = np.random.choice(len(pi), p=pi)
        return move, pi
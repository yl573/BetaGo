from MCTS import MCTS
from Shared.Functions import toggle_player
from GoGame.GoSimulator import GoSimulator, board_to_string
from GoGame.GoBackend import find_move
import numpy as np
import random


class MCTSAgent:
    def __init__(self,
                 model,
                 player,
                 size,
                 input_moves,
                 search_iters=50):

        self.size = size
        self.iters = search_iters
        self.model = model
        self.player = player
        self.input_moves = input_moves
        self.mcts = MCTS(
            self.model,
            self.player,
            self.size,
            self.input_moves)

    def select_move(self, boards, player):
        l = boards.shape[0]
        if self.input_moves > l:
            pad = np.zeros((self.input_moves - l, self.size, self.size))
            boards = np.vstack((pad, boards))
        boards = boards[-self.input_moves:]
        pi = self.mcts.search_for_pi(boards, player, iterations=self.iters)
        # Find position of next play that maximises pi
        move = np.random.choice(len(pi), p=pi)
        return move, pi


class RandomAgent:
    def __init__(self):
        pass

    def select_move(self, boards, player):
        n = boards.shape[1]
        game = GoSimulator(n)
        game.set_board_from_prev_boards(boards, player)
        legal = game.get_legal_moves().flatten()
        pi = np.append(legal, [1])
        pi = np.divide(pi, np.sum(pi))
        move = np.random.choice(len(pi), p=pi)
        return move, pi
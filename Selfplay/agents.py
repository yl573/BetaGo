
from MCTS import MCTS
from Shared.Functions import toggle_player
from GoGame.GoSimulator import GoSimulator, board_to_string
from GoGame.GoBackend import find_move
import numpy as np
import random

class MCTSAgent:
    
    def __init__(self, model, player, size, input_moves, search_iters=50, start_boards=None):

        self.size = size
        self.iters = search_iters
        if not start_boards:
            start_boards = np.zeros([input_moves,size,size])
        self.mcts = MCTS(model, player, size, input_moves, start_boards=start_boards)

    def select_move(self, boards, player): 

        move, color = find_move(
            board_to_string(boards[-2]), 
            board_to_string(boards[-1])
        )
        if move is None:
            move = self.size**2

        self.mcts.set_move(move)
        pi = self.mcts.search_for_pi(iterations=self.iters)
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
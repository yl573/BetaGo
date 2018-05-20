
from Model import Model
from MCTS import MCTS
from Shared.Consts import BLACK, WHITE
import numpy as np
from GoGame.GoSimulator import GoSimulator

b = np.array([[
    [0,1,-1,-1,-1],
    [1,1,-1,-1,-1],
    [0,1,-1,-1,-1],
    [1,1,-1,-1,-1],
    [0,-1,-1,-1,-1]
]])
boards = np.vstack((b,b,b,b))
# print(boards.shape)
player = BLACK

# class StubModel:
#     def __init__(self):
#         self.game = GoSimulator(5)

#     def eval(self, boards, next_player):
#         self.game.set_board_from_prev_boards(boards, next_player)
#         black_lead = self.game.black_score_lead()
#         V = black_lead/25
#         if next_player == WHITE:
#             V = -V
#         P = np.ones(26)
#         return P, V

# model = StubModel()

model = Model(5, 4, 'best_model.h5')
mcts = MCTS(model, 5, 4, 1, 0.1)

pi = mcts.search_for_pi(boards, player, iterations=110)

print(pi)
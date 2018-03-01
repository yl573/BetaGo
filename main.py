from MCTS import MCTS
import numpy as np
from Shared.Consts import BLACK, WHITE
from Shared.Functions import xy_to_index

class Model:
    def eval(self, board):
        P = np.ones(26)/26
        V = 0.1
        return P, V

model = Model()

boards = np.array([[
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,1,0,0,0],
    [0,0,0,0,0]
],[
    [0,0,0,0,0],
    [0,-1,0,0,0],
    [0,0,0,0,0],
    [0,1,0,0,0],
    [0,0,0,0,0]
]])

P = np.ones(26)/26
player = BLACK

mcts = MCTS(model, player, start_boards=boards)

pi = mcts.search_for_pi(iterations=250)
print(pi)

move = np.random.choice(len(pi), p=pi)
mcts.set_move(move)
print(move)

pi = mcts.search_for_pi(iterations=250)
print(pi)
from MCTS import MCTS
import numpy as np
from Shared.Consts import BLACK, WHITE

class Model:
    def eval(self, board):
        P =  np.ones((5,5))/25
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

P = np.ones((5,5))/25
player = BLACK

mcts = MCTS(model, player, start_boards=boards)

pi = mcts.search_for_pi(iterations=1000)
print(pi)

mcts.set_move((2,2))

pi = mcts.search_for_pi(iterations=1000)
print(pi)
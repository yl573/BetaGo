
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
player = BLACK

model = Model(5, 4, 'best_model.h5')
mcts = MCTS(model, 5, 4, 1, 0.1)

pi = mcts.search_for_pi(boards, player, iterations=110)

print(pi)
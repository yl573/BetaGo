from selfplay import selfPlay
from GoGame.GoSimulator import GoSimulator
from Shared.Consts import BLACK, WHITE

import numpy as np

class Model:
    def eval(self, board):
        P = np.ones(26)/26
        V = 0.1
        return P, V

model = Model()

game = GoSimulator(5)

player = BLACK

game_selfplay = selfPlay(model, player)

black_lead, boards = game_selfplay.playGame()

print(boards)
print('Black lead : ',black_lead)
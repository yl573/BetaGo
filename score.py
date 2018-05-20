from GoGame.GoSimulator import GoSimulator
import numpy as np
from Shared.Consts import BLACK, WHITE

game = GoSimulator(5)

player = WHITE
boards = np.array([
[[ 0, -1, -1, -1,  0],
 [-1,  0, -1, -1,  0],
 [-1, -1, -1, -1,  1],
 [-1,  0, -1,  0, -1],
 [-1, -1, -1, -1, -1]],
[[ 0, -1, -1, -1,  0],
 [-1,  0, -1, -1,  0],
 [-1, -1, -1, -1,  1],
 [-1,  0, -1,  0, -1],
 [-1, -1, -1, -1, -1]]
    ])

class StubModel:
    def eval(self, boards, player):
        game.set_board_from_prev_boards(boards, player)
        black_lead = game.black_score_lead()
        if black_lead == 0:
            V = 0
        elif player == BLACK:
            V = (black_lead > 0)*2 - 1
        else:
            V = (black_lead < 0)*2 - 1
        P = np.ones(26)
        return P, V

model = StubModel()
_, V = model.eval(boards, player)
print(player)
print(V)



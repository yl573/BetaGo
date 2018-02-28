from GoGame.GoSimulator import GoSimulator
from Shared.Consts import BLACK, WHITE
import numpy as np

game = GoSimulator(5)

boards = np.array([[
    [0,0,0,0,0],
    [0,0,1,0,0],
    [0,1,-1,1,0],
    [0,-1,0,-1,0],
    [0,0,-1,0,0]
],[
    [0,0,0,0,0],
    [0,0,1,0,0],
    [0,1,0,1,0],
    [0,-1,1,-1,0],
    [0,0,-1,0,0]
]])

game.set_board_from_prev_boards(boards, WHITE)
# or if there is no KO, you can use
# game.set_board(boards[-1], BLACK)

print(game.board)

# this function is currently faulty, it doesn't deal with ko
# but for the go player it makes no difference
legal = game.get_legal_moves()
print(legal, '\n')

board, next_player = game.play(2,2)
print(board, next_player, '\n')

black_lead = game.black_score_lead()
print(black_lead)

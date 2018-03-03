from GoGame.GoSimulator import GoSimulator
from GoGame import GoBackend
from Shared.Consts import BLACK, WHITE, num_to_char
import numpy as np

game = GoSimulator(5)

def board_to_string(board):
    board_flat = board.reshape(5**2)
    board_str = ''.join(list((map(lambda x: num_to_char[x], board_flat))))
    return board_str

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
print(game.board)
print(game.board.ko)
assert game.board.ko == 17

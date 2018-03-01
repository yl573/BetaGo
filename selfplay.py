from MCTS import MCTS
import numpy as np
from Shared.Consts import BLACK, WHITE
from Shared.Functions import xy_to_index
from GoGame.GoSimulator import GoSimulator
import random
import time


def addBoardtoBoards(board,boards,turn_counter):
    m = boards.shape[1]
    board_temp = np.reshape(board,-1)
    boards_temp = np.reshape(boards,-1)
    new_boards_temp = np.append(boards,board)
    new_boards = np.reshape(new_boards_temp, [turn_counter,m,m])
    return new_boards

def switchTurn(player):
    if player == WHITE:
        return BLACK
    elif player == BLACK:
        return WHITE


class Model:
    def eval(self, board):
        P = np.ones(26)/26
        V = 0.1
        return P, V

model = Model()

game = GoSimulator(5)

boards = np.array([[
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0]
],[
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0]
]])

P = np.ones(26)/26
player = BLACK

game.set_board_from_prev_boards(boards, player)
game.print_board()
# or if there is no KO, you can use
# game.set_board(boards[-1], BLACK)

print('+--------- START ---------+:\n')

turn_counter = 2
check_pass = 0

### --- Start game --- ###

while True:
    mcts = MCTS(model, player, start_boards=boards)
    pi = mcts.search_for_pi(iterations=250)
    # print(pi)

    # Find position of next play that maximises pi
    arg_pi_max = (np.argwhere(pi==np.max(pi)))
    arg_pi_max = arg_pi_max.flatten()

    arg_max = random.choice(arg_pi_max) # to deal with multiple maximums
    print('arg_max ',arg_max)

    
    if arg_max == 25: # PASS
        game.pass_move()
        check_pass = check_pass + 1
    else:
        move_y, move_x = divmod(arg_max, 5) # finds position of move on board and makes play
        print('Best move x:', move_x)
        print('Best move y:', move_y,'\n')
        # Plays the best move
        board, next_player = game.play(move_x,move_y)
        check_pass = 0

    turn_counter = turn_counter + 1

    # Add board to boards
    boards = addBoardtoBoards(board,boards,turn_counter)
    player = next_player

    game.set_board_from_prev_boards(boards, player)
    game.print_board()
    black_lead = game.black_score_lead()

    # Check win condition
    if check_pass >=2:
        break 

    # time.sleep(0.001)

black_lead = game.black_score_lead()
print(black_lead)
print(boards)
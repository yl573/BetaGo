from MCTS import MCTS
import numpy as np
from Shared.Consts import BLACK, WHITE
from Shared.Functions import xy_to_index
from GoGame.GoSimulator import GoSimulator
import random
import time

def addBoardtoBoards(board,boards,turn_counter):
    board_stack = board.reshape((1, *board.shape))
    new_boards = np.vstack((boards, board_stack))
    return new_boards

class Selfplay:

    def __init__(self, model, player, n=5, input_moves=4, start_boards=None, verbose=0):
        self.model = model
        self.game = GoSimulator(n)
        self.player = player
        self.n = n
        self.verbose = verbose
        self.input_moves = input_moves

    def maybe_print(self, *msg):
        if self.verbose:
            for m in msg:
                print(m, end='')
            print()

    def play_game(self, iters=50):
        n = self.n
        game = self.game
        player = self.player
        boards = np.zeros([self.input_moves,n,n])
        searched_pi = []

        game.set_board_from_prev_boards(boards, player)
        self.maybe_print(game.board)

        self.maybe_print('------------- START -------------\n')

        turn_counter = 2
        check_pass = 0
        mcts = MCTS(self.model, player, start_boards=boards)

        ### --- Start game --- ###

        while True:
            pi = mcts.search_for_pi(iterations=iters)
            self.maybe_print(pi)

            # Find position of next play that maximises pi
            move = np.random.choice(len(pi), p=pi)

            # arg_pi_max = (np.argwhere(pi==np.max(pi)))
            # arg_pi_max = arg_pi_max.flatten()

            # arg_max = random.choice(arg_pi_max) # to deal with multiple maximums
            # # self.maybe_print('arg_max ',arg_max)

            if move == 25: # PASS
                self.maybe_print(player, ' PASSES \n')
                board, next_player = game.pass_move()
                check_pass = check_pass + 1

            else:
                move_y, move_x = divmod(move, 5) # finds position of move on board and makes play
                self.maybe_print('Best move x:', move_x)
                self.maybe_print('Best move y:', move_y,'\n')
                # Plays the best move
                self.maybe_print(player, ' MOVES \n')
                board, next_player = game.play(move_x,move_y)
                check_pass = 0

            mcts.set_move(move)
            turn_counter = turn_counter + 1

            # Add board to boards
            boards = addBoardtoBoards(board,boards,turn_counter)
            searched_pi.append(pi)
            player = next_player

            game.set_board_from_prev_boards(boards, player)
            self.maybe_print(game.board)
            self.maybe_print('---------------------------------\n')
            black_lead = game.black_score_lead()

            # Check win condition
            if check_pass >=2:
                self.maybe_print('GAME OVER FROM 2 PASSES')
                break 

            if turn_counter == 5 * 5 * 2:
                self.maybe_print('GAME OVER FROM TURN LIMIT REACHED')
                break

            # time.sleep(0.001)
        self.maybe_print(player, ' LOST! HAHAHA! LOSER!')
        black_lead = game.black_score_lead()
        return black_lead, boards, searched_pi
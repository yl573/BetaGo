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

def print_winner(black_lead):
    if black_lead > 0:
        print('BLACK won by', black_lead)
    elif black_lead < 0:
        print('WHITE won by', -black_lead)
    else:
        print('The game is a draw')


class Selfplay_2models:

	def __init__(self, model1, model2, player, size, input_moves, start_boards=None, verbose=0):
		self.model1 = model1
		self.model2 = model2
		self.game = GoSimulator(size)
		self.player = player
		self.n = size
		self.verbose = verbose
		self.input_moves = input_moves

	def maybe_print(self, *msg):
		if self.verbose:
			for m in msg:
				print(m, end='')
			print()

	def makeMove(self, mcts, player, game, check_pass, iters):
	    pi = mcts.search_for_pi(iterations=iters)
	    # self.maybe_print(pi)

	    # Find position of next play that maximises pi
	    move = np.random.choice(len(pi), p=pi)

	    if move == self.n**2: # PASS
	        self.maybe_print(player, ' PASSES \n')
	        board, next_player = game.pass_move()
	        check_pass = check_pass + 1

	    else:
	        move_y, move_x = divmod(move, self.n) # finds position of move on board and makes play
	        # self.maybe_print('Best move x:', move_x)
	        # self.maybe_print('Best move y:', move_y,'\n')
	        # Plays the best move
	        self.maybe_print(player, ' MOVES \n')
	        board, next_player = game.play(move_x,move_y)
	        check_pass = 0

	    return pi, board, next_player, move, check_pass

	def play_game(self, iters=50):
		n = self.n
		game = self.game
		player = self.player
		boards = np.zeros([self.input_moves,n,n])
		searched_pi = []

		game.set_board_from_prev_boards(boards, player)
		self.maybe_print(game.board)

		self.maybe_print('------------- START -------------\n')
		turn_counter = 0
		check_pass = 0
		mcts1 = MCTS(self.model1, player, self.n, self.input_moves, start_boards=boards)
		mcts2 = MCTS(self.model2, player, self.n, self.input_moves, start_boards=boards)

        ### --- Start game --- ###

		while True:
			self.maybe_print('---------------------------------\n')
			self.maybe_print(game.board)
			if turn_counter % 2 == 0:
				pi, board, next_player, move, check_pass = self.makeMove(mcts1, player, game, check_pass, iters)
				mcts1.set_move(move)
				mcts2.set_move(move)
				print(pi)

			elif turn_counter % 2 == 1:
				pi, board, next_player, move, check_pass = self.makeMove(mcts2, player, game, check_pass, iters)
				mcts1.set_move(move)
				mcts2.set_move(move)
				print(pi)

			turn_counter = turn_counter + 1

			# Add board to boards
			boards = addBoardtoBoards(board,boards,turn_counter)
			searched_pi.append(pi)
			player = next_player

			game.set_board_from_prev_boards(boards, player)
			
			black_lead = game.black_score_lead()

			# Check win condition
			if check_pass >=2:
			    self.maybe_print('GAME OVER FROM 2 PASSES')
			    break 

			if turn_counter == self.n**2 * 2:
			    self.maybe_print('GAME OVER FROM TURN LIMIT REACHED')
			    break

		black_lead = game.black_score_lead()
		print_winner(black_lead)

		return black_lead, boards, searched_pi
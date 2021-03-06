from MCTS import MCTS
import numpy as np
from Shared.Consts import BLACK, WHITE
from Shared.Functions import xy_to_index
from GoGame.GoSimulator import GoSimulator
import random
import time



def print_winner(black_lead):
    if black_lead > 0:
        print('BLACK won by', black_lead)
    elif black_lead < 0:
        print('WHITE won by', -black_lead)
    else:
        print('The game is a draw')


class Selfplay:

    def __init__(self, agent1, agent2, player=BLACK, size=5, n_input=4):
        self.agents = [agent1, agent2]
        self.game = GoSimulator(size)
        self.player = player
        self.n = size
        self.n_input = n_input

    def maybe_print(self, *msg):
        if self.verbose:
            for m in msg:
                print(m, end='')
            print()

    def play_game(self, print_tree=False, verbose=0, greedy=False):
        n = self.n
        game = self.game
        player = self.player
        data = []
        boards_history = np.zeros((self.n_input, self.n, self.n))
        agent_id = 0
        self.verbose = verbose
        game.set_board(boards_history[-1], player, None)

        self.maybe_print('------------- START -------------\n')

        for step in range(self.n**2 * 2):

            agent = self.agents[agent_id]
            agent_id = 1 - agent_id

            if greedy:
                temp = 0.05
                diri = False
            elif step < 5:
                temp = 1
                diri = False
            else:
                temp = 0.05
                diri = True

            move, pi = agent.select_move(
                boards_history,
                player,
                temp,
                diri
            )

            if move == self.n**2: # PASS
                self.maybe_print(player, ' PASSES \n')
                board, next_player, end_condition = game.pass_move()

            else:
                move_y, move_x = divmod(move, self.n) # finds position of move on board and makes play
                self.maybe_print(player, ' MOVES \n')
                board, next_player, end_condition = game.play(move_x,move_y)

            self.maybe_print(game.board)
            self.maybe_print('---------------------------------\n')

            if print_tree and hasattr(agent, 'mcts'):
                agent.mcts.print_tree()

            # Append history
            data.append((
                boards_history[-self.n_input:],
                pi,
                player,
                None
            ))
            board_stack = board.reshape((1, *board.shape))
            boards_history = np.vstack((boards_history, board_stack))

            
            player = next_player

            if end_condition:
                self.maybe_print(end_condition)
                break

        black_lead = game.black_score_lead()
        if self.verbose:
            print_winner(black_lead)
        # to make lengths consistent, last boards doesn't trigger an action anyway
        outcomes = np.ones(len(data))
        if black_lead == 0:
            outcomes[:] = 0
        elif black_lead > 0:
            outcomes[1::2] = -1  # outcomes=[1,-1,1,-1...]
        else:
            outcomes[::2] = -1  # outcomes=[-1,1,-1,1...]
        for i, d in enumerate(data):
            new_d = list(d)
            new_d[3] = outcomes[i]
            data[i] = tuple(new_d)
        
        return np.array(data), black_lead
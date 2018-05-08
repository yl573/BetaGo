from Selfplay import Selfplay, RandomAgent, MCTSAgent
from Model import Model
from GoGame.GoSimulator import GoSimulator
from Shared.Consts import BLACK, WHITE
from Shared.Functions import toggle_player
import time

import numpy as np

N = 5
n_input = 4
player = BLACK
model_file = 'go_model_0.h5'

game = GoSimulator(N)

model = Model(saved_path=model_file, size=N, input_moves=n_input)
agent1 = MCTSAgent(model, player, N, n_input, search_iters=50)
agent2 = RandomAgent() #MCTSAgent(model, toggle_player(player), N, n_input, search_iters=50)

game_selfplay = Selfplay(agent1, agent2, BLACK, N, verbose=1)

black_score_allgames = []
boards_across_allgames = []


t0 = time.time()
black_lead, board_history, pi_history = game_selfplay.play_game()
t1 = time.time()

# print(black_lead)
# print(board_history.shape)
# print(len(pi_history))

# agent1.mcts.print_tree()

print('Time taken (secs): ', t1 - t0)
print('Number of moves: ', len(board_history))

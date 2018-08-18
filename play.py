from Selfplay import Selfplay, RandomAgent, MCTSAgent, UserAgent
from Model import Model
from GoGame.GoSimulator import GoSimulator
from Shared.Consts import BLACK, WHITE
from Shared.Functions import toggle_player, writer
import time
import sys
import numpy as np

N = 5
n_input = 4
player = BLACK

game = GoSimulator(N)

model = Model(saved_path='michael_best_model.h5', size=N, input_moves=n_input)
# model = Model(size=N, input_moves=n_input)

agent1 = MCTSAgent(model, N, n_input, 110, cpuct=1)
agent2 = UserAgent()

game_selfplay = Selfplay(agent1, agent2, BLACK, N, n_input)

t0 = time.time()
data, black_lead = game_selfplay.play_game(print_tree=False, verbose=1, greedy=False)
t1 = time.time()

if black_lead > 0:
    print('Black won by', black_lead)
elif black_lead < 0:
    print('White won by', -black_lead)
else:
    print('The game is a draw')

print('Time taken (secs): ', t1 - t0)
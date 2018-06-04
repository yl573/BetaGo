from Selfplay import Selfplay, RandomAgent, MCTSAgent
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

sys.stdout = writer('out.log', sys.stdout)

game = GoSimulator(N)

# model1 = Model(saved_path='best_model.h5', size=N, input_moves=n_input)
model1 = Model(saved_path='Trained_Models/pretrain.h5', size=N, input_moves=n_input)

agent1 = MCTSAgent(model1, N, n_input, 110, cpuct=1)
agent2 = RandomAgent()#MCTSAgent(model2, N, n_input, 110, cpuct=5)

game_selfplay = Selfplay(agent1, agent2, BLACK, N, n_input)

t0 = time.time()
data, black_lead = game_selfplay.play_game(print_tree=False, verbose=1, greedy=True)
t1 = time.time()

print('Time taken (secs): ', t1 - t0)

print(data)


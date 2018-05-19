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

model_file = 'pretrain.h5'

sys.stdout = writer('out.log', sys.stdout)

game = GoSimulator(N)

model = Model(saved_path=model_file, size=N, input_moves=n_input)
agent1 = MCTSAgent(model, player, N, n_input, 110, cpuct=1, temp=1)
agent2 = RandomAgent()

game_selfplay = Selfplay(agent1, agent2, BLACK, N, n_input)

t0 = time.time()
board_history, pi_history,_ ,_ ,black_lead = game_selfplay.play_game(print_tree=True, verbose=1)
t1 = time.time()

print('Time taken (secs): ', t1 - t0)
print('Number of moves: ', len(board_history))

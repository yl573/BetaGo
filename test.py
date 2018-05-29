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

#model1 = Model(saved_path='best_model_edward.h5', size=N, input_moves=n_input)
model2 = Model(saved_path='pretrain_21.h5', size=N, input_moves=n_input)

agent1 = RandomAgent()#MCTSAgent(model1, N, n_input, 110, cpuct=1)
agent2 = MCTSAgent(model2, N, n_input, 110, cpuct=1)

game_selfplay = Selfplay(agent1, agent2, BLACK, N, n_input)

t0 = time.time()
board_history, pi_history,_ ,_ ,black_lead = game_selfplay.play_game(print_tree=False, verbose=1, greedy=False)
t1 = time.time()

print('Time taken (secs): ', t1 - t0)
print('Number of moves: ', len(board_history))

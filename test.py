from Selfplay import Selfplay, RandomAgent, MCTSAgent
# from Model import Model
from GoGame.GoSimulator import GoSimulator
from Shared.Consts import BLACK, WHITE
import time

import numpy as np

N = 5
n_input = 4

for i in range(2000):

    game = GoSimulator(N)
    agent1 = RandomAgent()
    agent2 = RandomAgent()

    game_selfplay = Selfplay(agent1, agent2, BLACK, N, n_input, verbose=0)

    black_score_allgames = []
    boards_across_allgames = []

    t0 = time.time()
    black_lead, board_history, pi_history = game_selfplay.play_game(50)
    t1 = time.time()

    print('Time taken (secs): ', t1 - t0)
    print('Number of moves: ', len(board_history))
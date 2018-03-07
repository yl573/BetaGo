from Selfplay import Selfplay
from Model import Model
from GoGame.GoSimulator import GoSimulator
from Shared.Consts import BLACK, WHITE
import time


import numpy as np

game = GoSimulator(5)

# Starting player
player = BLACK 

model = Model()
game_selfplay = Selfplay(model, player, verbose=1)

black_score_allgames = []
boards_across_allgames = []

# Start self play for 1 games
t0 = time.time()
black_lead, boards, pi = game_selfplay.play_game(10)
t1 = time.time()

print('Time taken (secs): ', t1 - t0)
print('Number of moves: ', len(boards))
print('Black leads by : ',black_lead)
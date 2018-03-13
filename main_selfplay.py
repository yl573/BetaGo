from Selfplay import Selfplay
from Model import Model
from GoGame.GoSimulator import GoSimulator
from Shared.Consts import BLACK, WHITE
import time


import numpy as np

N = 5
n_input = 4

game = GoSimulator(N)

# Starting player
player = BLACK 

model = Model(saved_path='go_model_9.h5', size=N, input_moves=n_input) #if there is a saved model
#model = Model(size=N, input_moves=n_input)
game_selfplay = Selfplay(model, player, size=N, input_moves=n_input, verbose=1)

black_score_allgames = []
boards_across_allgames = []

# Start self play for 1 games
t0 = time.time()
black_lead, boards, pi = game_selfplay.play_game(50)
t1 = time.time()

#model.save('model.h5')

print('Time taken (secs): ', t1 - t0)
print('Number of moves: ', len(boards))
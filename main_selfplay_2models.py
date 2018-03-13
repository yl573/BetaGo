from Selfplay import Selfplay_2models
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

# model1 = Model(saved_path='model.h5', size=N, input_moves=n_input) #if there is a saved model
model1 = Model(size=N, input_moves=n_input)
model2 = Model(size=N, input_moves=n_input)
game_selfplay = Selfplay_2models(model1, model2, player, size=N, input_moves=n_input, verbose=1)

black_score_allgames = []
boards_across_allgames = []

# Start self play for 1 games
t0 = time.time()
black_lead, boards, pi = game_selfplay.play_game(100)
t1 = time.time()

model1.save('model1.h5')
model2.save('model2.h5')

print('Time taken (secs): ', t1 - t0)
print('Number of moves: ', len(boards))
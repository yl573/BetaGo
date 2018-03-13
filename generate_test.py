from Selfplay import Selfplay
from GoGame.GoSimulator import GoSimulator
from Shared.Consts import BLACK, WHITE
from Training.Data import Data

import numpy as np

class Model:
    def __init__(self, size, input_moves):
        self.size = size
        self.input_moves = input_moves
    def eval(self, boards, next_player):
        P = np.ones(26)/26
        V = 0.1
        return P, V

# Starting player
model = Model(5, 4)
player = BLACK 

trainer = Data(model)

trainingset, piset, outcomeset = trainer.generate(num_samples=12, augment=True)

print (np.shape(trainingset))
print (trainingset[-1])
print (np.reshape(piset[:,:25], (12,5,5)))
print ("OUTCOME")
print (outcomeset)
from Selfplay import Selfplay
from GoGame.GoSimulator import GoSimulator
from Shared.Consts import BLACK, WHITE
from Training.Data import Data

import numpy as np

class Model:
    def eval(self, board):
        P = np.ones(26)/26
        V = 0.1
        return P, V

# Starting player
model = Model()
player = BLACK 

trainer = Data(model)

trainingset = trainer.Generate(num_samples=4)

print (np.shape(trainingset))
print (trainingset[-1])
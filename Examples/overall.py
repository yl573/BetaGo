from Selfplay import Selfplay
from GoGame.GoSimulator import GoSimulator
from Shared.Consts import BLACK, WHITE
from Training.DataGenerator import DataGenerator

from Model.model import Model

import numpy as np

# Set Constants
SIZE = 5
INPUT_MOVES = 3
PLAYER = BLACK
NUM_SAMPLES = 100

# Initialize Model
go_model = Model(SIZE, INPUT_MOVES)

# Initialize Trainer
data_generator = DataGenerator(go_model, player=PLAYER, size=SIZE, input_moves=INPUT_MOVES)

# Generate 100 number of samples
print ("Generating Sample Games")
training_set, pi_set, black_leads_set = data_generator.generate(num_samples=6)

print ("Fitting Model")
go_model.model.fit(training_set, [pi_set, black_leads_set], epochs=1, batch_size=2)

# print (np.shape(trainingset))
# print (trainingset[-1])
# print (np.shape(piset))
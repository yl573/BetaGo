from Selfplay import Selfplay
from GoGame.GoSimulator import GoSimulator
from Shared.Consts import BLACK, WHITE
from Training.DataGenerator import DataGenerator
from Training.Trainer import Trainer

from Model import Model

import numpy as np

# Set Constants
SIZE = 5
INPUT_MOVES = 4
INPUT_MOVES_MODEL = 2

PLAYER = BLACK
NUM_SAMPLES = 10
TRAINING_STEPS=15
EPOCHS = 10
BATCH_SIZE=1

# Initialize Model
go_model = Model(SIZE, INPUT_MOVES)

# Initialise Trainer

go_trainer = Trainer(go_model, SIZE, INPUT_MOVES)

go_trainer.train(TRAINING_STEPS, NUM_SAMPLES, augment=False, epochs=EPOCHS, batch_size=BATCH_SIZE)

print ("Done")

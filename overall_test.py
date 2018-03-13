from Selfplay import Selfplay
from GoGame.GoSimulator import GoSimulator
from Shared.Consts import BLACK, WHITE
from Training.Data import Data
from Training.Trainer import Trainer

from Model.model import Model

import numpy as np

# Set Constants
SIZE = 5
INPUT_MOVES = 3
PLAYER = BLACK
NUM_SAMPLES = 6
TRAINING_STEPS=4
EPOCHS = 3
BATCH_SIZE=2

# Initialize Model
go_model = Model(SIZE, INPUT_MOVES)

# Initialise Trainer

go_trainer = Trainer(go_model, SIZE, INPUT_MOVES)

go_trainer.train(TRAINING_STEPS, NUM_SAMPLES, epochs=EPOCHS, batch_size=BATCH_SIZE)

print ("Done")

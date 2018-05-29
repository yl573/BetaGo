import argparse
import os
import random
import sys

from Selfplay import Selfplay, RandomAgent, MCTSAgent
from Model import Model
from GoGame.GoSimulator import GoSimulator
from Shared.Consts import BLACK, WHITE
import time

from Training.DataGenerator import DataGenerator
from Training.Trainer import Trainer

import numpy as np

# Set Constants
SIZE = 5
INPUT_MOVES = 4
INPUT_MOVES_MODEL = 2

# Initialize Model
go_model = Model(SIZE, INPUT_MOVES)
go_model.fit()
print('done')
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

PLAYER = BLACK
NUM_GAMES = 10
TRAINING_STEPS = 5
EPOCHS = 2
BATCH_SIZE = 1
SEARCH_ITERS = 110
CPUCT = 10
DATA_SAVE_PATH = 'data.pkl'

parser = argparse.ArgumentParser(description='''
    Train the BetaGo network''')

parser.add_argument(
    '-b',
    '--batch_size',
    action='store',
    type=int,
    default=BATCH_SIZE,
    help='''Batch size for training and validation''')
parser.add_argument(
    '-e',
    '--epochs',
    action='store',
    type=int,
    default=EPOCHS,
    help='''Number of iterations for which training will be performed''')

args = parser.parse_args()

# Initialize Model
go_model = Model(SIZE, INPUT_MOVES)

# Initialise Trainer
go_trainer = Trainer(go_model, SIZE, INPUT_MOVES, SEARCH_ITERS, CPUCT)

go_trainer.train(
    TRAINING_STEPS,
    NUM_GAMES,
    augment=False,
    epochs=EPOCHS,
    batch_size=args.batch_size,
    data_save_path=DATA_SAVE_PATH)

print("Done")

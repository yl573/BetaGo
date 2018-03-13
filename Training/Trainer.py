import numpy as np
from Selfplay import Selfplay
from GoGame.GoSimulator import GoSimulator
from Shared.Consts import BLACK, WHITE
from .Data import Data

class Trainer:
    def __init__(self, model, size, input_moves):
        self.size = size
        self.input_moves = input_moves
        
        self.best_model = model
        
        print ("Initializing Trainer")
        self.data = Data(model, player=BLACK, size=size, input_moves=input_moves)
    
    def train(self, training_steps, num_samples, epochs=3, batch_size=2):
        
        for i in range(training_steps):
            curr_model = self.best_model
            self.data.update_model(curr_model)
            
            training_set, pi_set, black_leads_set = self.data.generate(num_samples)

            curr_model.model.fit(training_set, [pi_set, black_leads_set], epochs=epochs, batch_size=batch_size)

            if self.evaluate_against_best(curr_model):
                print ("New Model is better")
                self.best_model = curr_model
            else:
                print ("New Model not better")       
        
    def evaluate_against_best(self, model):
        ###########
        return True
        
    def generate_data(self, num_samples):
        return self.trainer.Generate(num_samples)
import numpy as np
from Selfplay import Selfplay
from GoGame.GoSimulator import GoSimulator
from Shared.Consts import BLACK, WHITE
from .DataGenerator import DataGenerator
import dill

class Trainer:
    def __init__(self, model, size, input_moves, search_iters, cpuct):
        self.size = size
        self.input_moves = input_moves
        self.best_model = model
        
        print ("Initializing Trainer")
        self.data_generator = DataGenerator(model, search_iters, cpuct, player=BLACK, size=size, input_moves=input_moves)
    
    def train(self, training_steps, num_games, augment=False, epochs=2, batch_size=2, data_save_path=None):
        data = {
            'boards': [],
            'pi': [],
            'outcome': [],
            'player': []
        }
        for i in range(training_steps):

            print('Iteration', i)

            curr_model = self.best_model
            self.data_generator.update_model(curr_model)
            
            boards, pi, outcome, player = self.data_generator.generate(num_games, augment)

            if data_save_path is not None:
                data['boards'].append(boards)
                data['pi'].append(pi)
                data['outcome'].append(outcome)
                data['player'].append(player)

            curr_model.fit(boards, pi, outcome, player, epochs)

            if self.evaluate_against_best(curr_model):
                print ("New Model is better")
                self.best_model = curr_model
            else:
                print ("New Model not better") 
        
            self.best_model.save('go_model_'+str(i)+'.h5')

        if data_save_path is not None:
            print('Saving to', data_save_path)
            with open(data_save_path, "wb") as f:
                dill.dump(data, f)
        
    def evaluate_against_best(self, model):
        ###########
        return True
        
    # def generate_data(self, num_samples):
    #     return self.trainer.Generate(num_samples)
#from MCTS import MCTS
import numpy as np
#from Shared.Consts import BLACK, WHITE
#from Shared.Functions import xy_to_index
from Selfplay import Selfplay
from GoGame.GoSimulator import GoSimulator
from Shared.Consts import BLACK, WHITE

import numpy as np

class Data:
    
    def __init__(self, model, player=BLACK, size=5, input_moves=4):
        self.model = model
        self.start_player = player
        self.size = size
        self.input_moves = input_moves
       
        # Initialise Selfplay Class
        self.game_selfplay = Selfplay(model, player, size, input_moves)
    
    def update_model(self, model):
        self.model = model

    def generate(self, num_samples=50, augment=True):
        # Prepare Variables
        model = self.model
        n = self.size
        m = self.input_moves
        num_moves = 2*m
        curr_player = 0
        
        # Prepare padding (given buffer comes from buffer from SelfPlay. Obsolete?)
        given_buffer = 3
        padding = np.zeros((num_moves-1-given_buffer, n, n))
        buffer = np.zeros((num_moves-1, n, n))
        
        # Placeholders
        training_set = np.ones((num_samples, num_moves+1, n, n))
        pi_set = np.ones((num_samples, n*n+1))
        black_leads_set = np.ones((num_samples, 1))
        
        # Generate Training set
        for i in range(num_samples):
            
            # Play one game
            black_leads, boards, pi = self.game_selfplay.play_game()
            
            print (boards[:6])
            
            # Determine length of game and pad boards
            max_move = np.shape(boards)[0]
            padded_boards = np.concatenate((padding, boards), axis=0)
            
            # Randomly choose a move
            chosen_move = np.random.choice(max_move - given_buffer - 1)
            padded_chosen_move = chosen_move + num_moves - 1
            
            # Extract moves
            sampled_moves = padded_boards[padded_chosen_move:padded_chosen_move-num_moves:-1, :, :]
            
            # Determine current player
            if chosen_move % 2 == 0:
                curr_player = 1
            else:
                curr_player = 0
            player_array = curr_player*np.ones((1, n,n))
            
            # Concatenate current player with sampled moves
            sampled_set = np.concatenate((sampled_moves, player_array), axis=0)
            
            # Add values to placeholders
            training_set[i,:,:,:] = sampled_set
            pi_set[i, :] = pi[chosen_move]
            black_leads_set[i] = black_leads
            # print (chosen_move)
        
        return training_set, pi_set, black_leads_set
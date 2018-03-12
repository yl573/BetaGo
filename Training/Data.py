#from MCTS import MCTS
import numpy as np
#from Shared.Consts import BLACK, WHITE
#from Shared.Functions import xy_to_index
from Selfplay import Selfplay
from GoGame.GoSimulator import GoSimulator
from Shared.Consts import BLACK, WHITE

import numpy as np

class Data:
    
    def __init__(self, model, player=BLACK, n=5, m=4):
        self.model = model
        self.start_player = player
        self.n = n
        self.m = m
        
        # Initialise Selfplay Class
        self.game_selfplay = Selfplay(model, player)

#     def SelfPlay(self):
#         n = self.n
#         m = self.m
#         model = self.model
        
        
#         #game_history = np.random.choice([-1,0,1], (30, n, n))
#         game_history = np.zeros((15,n,n))
        
#         board = np.zeros((n,n))
#         for i in range(15):
#             es = np.where(board==0)
#             rid = np.random.choice(np.shape(es)[-1])
            
#             if i%2==0:
#                 board[es[0][rid], es[1][rid]] = 1
#             else:
#                 board[es[0][rid], es[1][rid]] = -1
                
#             game_history[i, :, :] = board
        
        
#         outcome = np.random.choice([-1,0,1], 1)
        
#         # first entry in game_history should be first move, NOT empty board
#         return game_history, outcome

    def Generate(self, num_samples=50, augment=True):
        
        model = self.model
        n = self.n
        m = self.m
        num_moves = 2*m
        
        buffer = np.zeros((num_moves-1, n, n))
        
        training_set = np.ones((num_samples, num_moves+1, n, n))

        for i in range(num_samples):

            outcome, game_history = self.game_selfplay.playGame()
            
            #print (np.shape(game_history))
            
            max_move = np.shape(game_history)[0]
            
            chosen_move = np.random.choice(max_move-2)+1
            #chosen_move = max_move-1
            
            sampled_moves_first = game_history[chosen_move:max([0, chosen_move-num_moves]):-1, :, :]
            sampled_moves_second = buffer[:max([0,num_moves-chosen_move]), :, :] 
            
            sampled_moves = np.concatenate((sampled_moves_first, sampled_moves_second), axis=0)
            
            outcome_array = outcome*np.ones((1, n,n))
            
            sampled_set = np.concatenate((sampled_moves, outcome_array), axis=0)
            
            training_set[i,:,:,:] = sampled_set
        
        #print ("CHOSEN: ",chosen_move,", MAX: ",max_move)
        
        return training_set
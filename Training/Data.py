    #from MCTS import MCTS
import numpy as np
#from Shared.Consts import BLACK, WHITE
#from Shared.Functions import xy_to_index
from Selfplay import Selfplay, MCTSAgent, RandomAgent
from GoGame.GoSimulator import GoSimulator
from Shared.Consts import BLACK, WHITE

import numpy as np

class Data:

    def __init__(self, model, search_iters, cpuct, player=BLACK, size=5, input_moves=4):
        # print ( model.input_moves)
        # print (size, input_moves)
        self.model = model
        self.start_player = player
        self.size = size
        self.input_moves = input_moves
        self.agent1 = MCTSAgent(model, player, size, input_moves, search_iters, cpuct)
        self.agent2 = MCTSAgent(model, player, size, input_moves, search_iters, cpuct)
        # self.agent2 = RandomAgent()

        # Initialise Selfplay Class
        self.game_selfplay = Selfplay(self.agent1, self.agent2, player, size, input_moves)

    def update_model(self, model):
        self.agent1.model = model

    def generate(self, num_samples=100, augment=False):
        # Prepare Variables
        model = self.model
        n = self.size
        m = self.input_moves
        num_moves = m*2
        curr_player = 0
        outcome = 0

        if augment:
            augment_factor = 4
            sampled_aug = np.zeros((3, num_moves+1, n, n))
            pi_mat_aug = np.zeros((3,n,n))
            pi_aug = np.zeros((3, n*n+1))
        else:
            augment_factor = 1

#         # Prepare padding (given buffer comes from buffer from SelfPlay. Obsolete?)
#         given_buffer = 3
#         padding = np.zeros((num_moves-1-given_buffer, n, n))
#         buffer = np.zeros((num_moves-1, n, n))

        # Placeholders
        training_set = np.ones((num_samples, num_moves+1, n, n))
        pi_set = np.ones((num_samples, n*n+1))
        outcome_set = np.ones((num_samples, 1))

        # Generate Training set
        for j in range(int(num_samples/augment_factor)):

            if augment:
                i = j*4
            else:
                i = j
            # print (i)

            print("Game ", j)
            black_leads, boards, pi = self.game_selfplay.play_game()
            print ("Number of Moves: ", len(pi))
            print()

            # print (np.size(boards))
            # print ("..........")

            # Determine length of game and pad boards
            max_move = np.shape(pi)[0]

            # print ("max_move:", max_move)

            # Randomly choose a move
            chosen_move = np.random.choice(max_move)
            padded_chosen_move = chosen_move+num_moves-1

            # Extract moves
            padded_boards = np.concatenate((np.zeros((2*m, n, n)), boards), axis=0)

            start_pad = padded_chosen_move-num_moves

            sampled_moves = padded_boards[padded_chosen_move:None if start_pad<0 else start_pad:-1, :, :]

            # Determine outcome wrt BLACK
            if black_leads != 0:
                outcome = (black_leads/np.abs(black_leads))

            # Determine current player
            if chosen_move % 2 == 0:
                curr_player = 1
            else:
                curr_player = 0
                outcome = -outcome
            player_array = curr_player*np.ones((1, n,n))

            # Concatenate current player with sampled moves
            sampled_set = np.concatenate((sampled_moves, player_array), axis=0)

            # print ("Chosen_move: ",chosen_move)
            # print ("")
            # print ("Sampled_set: ",np.shape(sampled_set))

            # Add values to placeholders
            training_set[i,:,:,:] = sampled_set
            pi_set[i, :] = pi[chosen_move]
            outcome_set[i] = outcome
            # print (chosen_move)
            # print (np.shape(pi[chosen_move]))
            #print (np.reshape(pi[chosen_move][0:25], (5,5)))

            if augment:
                pi_mat = np.reshape(pi[chosen_move][0:25], (5,5))
                num_rot = np.random.choice([1,2,3], 1)

                sampled_aug[0,:,:,:] = np.rot90(sampled_set, num_rot, axes=(1,2))
                sampled_aug[1,:,:,:] = np.flip(sampled_set, axis=1)
                sampled_aug[2,:,:,:] = np.flip(sampled_set, axis=2)

                pi_aug[:,25] = pi[chosen_move][25]

                pi_mat_aug = np.rot90(pi_mat, num_rot, axes=(0,1))
                pi_aug[0,:25] = np.reshape(pi_mat_aug, 25)

                pi_mat_aug = np.flip(pi_mat, axis=0)
                pi_aug[1,:25] = np.reshape(pi_mat_aug, 25)

                pi_mat_aug = np.flip(pi_mat, axis=1)
                pi_aug[2,:25] = np.reshape(pi_mat_aug, 25)

                for kk in range(3):
                    training_set[i+kk+1,:,:,:] = sampled_aug[kk,:,:,:]
                    pi_set[i+kk+1,:] = pi_aug[kk,:]
                    outcome_set[i+kk+1] = outcome
                    # print (i+kk+1)


        return training_set, pi_set, outcome_set

    #from MCTS import MCTS
import numpy as np
#from Shared.Consts import BLACK, WHITE
#from Shared.Functions import xy_to_index
from Selfplay import Selfplay, MCTSAgent, RandomAgent
from GoGame.GoSimulator import GoSimulator
from Shared.Consts import BLACK, WHITE

import numpy as np

class DataGenerator:

    def __init__(self, model, search_iters, cpuct, player=BLACK, size=5, input_moves=4):
        # print ( model.input_moves)
        # print (size, input_moves)
        self.model = model
        self.start_player = player
        self.size = size
        self.input_moves = input_moves
        self.agent1 = MCTSAgent(model, player, size, input_moves, search_iters, cpuct)
        # self.agent2 = MCTSAgent(model, player, size, input_moves, search_iters, cpuct)
        self.agent2 = RandomAgent()

        # Initialise Selfplay Class
        self.game_selfplay = Selfplay(self.agent1, self.agent2, player, size, input_moves)

    def update_model(self, model):
        self.agent1.model = model
        # self.agent2.model = model

    def generate(self, n_games, augment=False):

        boards_his = np.zeros((1, self.size, self.size))
        pi_his = np.zeros((1, self.size**2+1))
        out_his = np.array([])
        player_his = np.array([])
        for i in range(n_games):

            print("Generating game", i)
            black_leads, boards, pi, player = self.game_selfplay.play_game()
            print ("Game ended, number of moves: ", len(pi))
            print()

            outcome = np.ones(len(pi))       
            if black_leads < 0:
                outcome[1::2] = -1 # outcomes=[1,0,1,0...]
            else:
                outcome[::2] = -1 # outcomes=[0,1,0,1...]

            boards_his = np.vstack((boards_his, boards))
            pi_his = np.vstack((pi_his, pi))
            out_his = np.concatenate((out_his, outcome))
            player_his = np.concatenate((player_his, player))

        return boards_his[1:], pi_his[1:], out_his, player_his # first one is padding

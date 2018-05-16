import numpy as np
import dill
from Selfplay import Selfplay, MCTSAgent
from Shared.Consts import BLACK, WHITE
from Model import Model

class Trainer:
    def __init__(self, model_file=None, benchmark_file=None, size=5, input_moves=4, search_iters=110, cpuct=1):
        self.size = size
        self.input_moves = input_moves
        challenger_model = Model(size, input_moves, model_file)
        benchmark_model = Model(size, input_moves, benchmark_file)
        self.challenger = MCTSAgent(challenger_model, BLACK, size, input_moves, search_iters, cpuct)
        self.benchmark = MCTSAgent(benchmark_model, WHITE, size, input_moves, search_iters, cpuct)

    def play_games_and_train(self, num_games=50, win_thresh=0.6, verbose=0, epochs=3, save_name=None):
        data, win_prob = self.generate_games(num_games, verbose) 
        print('Challenger wins with', win_prob, 'probability')
        if win_prob >= win_thresh:
            print("Challenger outperformed benchmark, setting benchmark to challenger")
            self.challenger.model.save('best_model.h5')
            # set the benchmark agent's model to the challenger's model
            benchmark_model = Model(self.size, self.input_moves, 'best_model.h5')
            self.benchmark.model = benchmark_model
        else:
            print("Challenger cannot outperform benchmark")

        self.train_agent(self.challenger, data, epochs)

        if save_name:
            self.save_data(data, save_name)
        
    def save_data(self, data, save_name):
        path = save_name
        print('Saving to', path)
        with open(path, "wb") as f:
            dill.dump(data, f)

    def train_agent(self, agent, data, epochs):
        ind = np.random.permutation(len(data['outcomes']))
        agent.model.fit(
            data['boards'][ind], 
            data['pi'][ind], 
            data['outcomes'][ind], 
            data['players'][ind],
            epochs
        )

    def generate_games(self, num_games, verbose):
        selfplay = Selfplay(self.challenger, self.benchmark)
        boards_history = np.zeros((1, self.size, self.size))
        pi_history = np.zeros((1, self.size**2 + 1))
        outcome_history = np.array([])
        player_history = np.array([])
        black_wins = 0
        for i in range(num_games):
            if verbose:
                print("Generating game", i)
            black_leads, boards, pi, player = selfplay.play_game(verbose=verbose)
            if verbose:
                print("Game ended, number of moves: ", len(pi))
                print()

            outcome = np.ones(len(pi))
            if black_leads == 0:
                outcome[:] = 0
                black_wins += 0.5
            elif black_leads > 0:
                outcome[1::2] = -1  # outcomes=[1,-1,1,-1...]
                black_wins += 1
            else:
                outcome[::2] = -1  # outcomes=[-1,1,-1,1...]
                

            boards_history = np.vstack((boards_history, boards))
            pi_history = np.vstack((pi_history, pi))
            outcome_history = np.concatenate((outcome_history, outcome))
            player_history = np.concatenate((player_history, player))
            win_prob = black_wins/num_games

        data = {
            'boards': boards_history[1:], # first one is padding
            'pi': pi_history[1:], # first one is padding
            'outcomes': outcome_history, 
            'players': player_history
        }
        return data, win_prob



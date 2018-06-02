import numpy as np
import dill
from Selfplay import Selfplay, MCTSAgent
from Shared.Consts import BLACK, WHITE
from Model import Model
from tqdm import tqdm
from MCTS.Augment import augment_dataset


class Trainer:
    def __init__(self,
                 model_file=None,
                 benchmark_file=None,
                 buffer_len=8192,
                 init_buffer=[],
                 size=5,
                 input_moves=4,
                 search_iters=110,
                 cpuct=1):
        self.size = size
        self.input_moves = input_moves
        challenger_model = Model(size, input_moves, model_file)
        benchmark_model = Model(size, input_moves, benchmark_file)
        self.challenger = MCTSAgent(challenger_model, size, input_moves,
                                    search_iters, cpuct)
        self.benchmark = MCTSAgent(benchmark_model, size, input_moves,
                                   search_iters, cpuct)
        self.buffer_len = buffer_len
        self.buffer = None
        self.fill_buffer(init_buffer)

    def fill_buffer(self, init_buffer):
        for path in init_buffer:
            print('Loading', path, 'into buffer')
            with open(path, "rb") as f:
                data = dill.load(f)
                self.add_to_replay_buffer(data)

    def add_to_replay_buffer(self, data):
        if self.buffer is None:
            self.buffer = data
        else:
            self.buffer = np.vstack((self.buffer, data))

        print('Replay buffer length', self.buffer.shape[0])

    def sample_from_replay_buffer(self, samples):
        ind = np.random.randint(0, high=(len(self.buffer)-1), size=samples)
        return self.buffer[ind]

    def play_games_and_train(self,
                             num_games=100,
                             batch_size=1024,
                             num_evals=20,
                             win_thresh=0.6,
                             verbose=0,
                             epochs=3,
                             augment=True,
                             save_name=None):
        data = self.generate_games(num_games, verbose)
        if save_name:
            self.save_data(data, save_name)
        self.add_to_replay_buffer(data)
        training_data = self.sample_from_replay_buffer(batch_size)
        if augment:
            training_data = augment_dataset(training_data)
            
        self.train_challenger(training_data, epochs)
        win_prob = self.evaluate_challenger(num_evals, verbose)
        print('Challenger wins with probability', win_prob)

        if win_prob >= win_thresh:
            print("Challenger outperformed benchmark, setting benchmark to challenger")
            self.challenger.model.save('best_model.h5')
            benchmark_model = Model(self.size, self.input_moves, 'best_model.h5')
            self.benchmark.model = benchmark_model
            
        # elif win_prob <= 0.35:
        #     print('Challenger is significantly worse, resetting it to benchmark')
        #     challenger_model = Model(self.size, self.input_moves, 'best_model.h5')
        #     self.challenger.model = challenger_model   

        else:
            print("Challenger cannot outperform benchmark")

    def save_data(self, data, save_name):
        path = save_name
        print('Saving to', path)
        with open(path, "wb") as f:
            dill.dump(data, f)

    def train_challenger(self, data, epochs):
        ind = np.random.permutation(len(data))
        self.challenger.model.fit(data[ind], epochs)

    def evaluate_challenger(self, num_games, verbose):
        black_wins = 0
        selfplay = Selfplay(self.challenger, self.benchmark)
        print("Evaluating")
        for i in tqdm(range(num_games)):
            _, black_leads = selfplay.play_game(verbose=verbose, greedy=True)
            selfplay = self.swap_players(selfplay)
            if black_leads == 0:
                black_wins += 0.5
            elif black_leads > 0:
                black_wins += 1

        return black_wins / num_games

    def swap_players(self, selfplay):
        temp_agent = selfplay.agents[0]
        selfplay.agents[0] = selfplay.agents[1]
        selfplay.agents[1] = temp_agent
        return selfplay

    def generate_games(self, num_games, verbose):
        selfplay = Selfplay(self.benchmark, self.benchmark)
        data = None

        print("Generating")
        for i in tqdm(range(num_games)):
            if verbose:
                print("Game", i)
            game_data, _ = selfplay.play_game(verbose=verbose)
            selfplay = self.swap_players(selfplay)
            if verbose:
                print("Game ended, number of moves: ", len(game_data))
                print()
            if data is None:
                data = game_data
            else:
                data = np.vstack((data, game_data))

        return data

import numpy as np
import dill
from Selfplay import Selfplay, MCTSAgent
from Shared.Consts import BLACK, WHITE
from Model import Model
from tqdm import tqdm


class Trainer:
    def __init__(self,
                 model_file=None,
                 benchmark_file=None,
                 buffer_len=4096,
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
        # assert (len(data['boards']) == len(data['pi']) == len(data['outcomes']) == len(data['players']))

        if not self.buffer:
            self.buffer = data
        else:
            self.buffer['boards'] = np.vstack(
                (self.buffer['boards'], data['boards']))[-self.buffer_len:]
            self.buffer['pi'] = np.vstack((self.buffer['pi'],
                                           data['pi']))[-self.buffer_len:]
            self.buffer['outcomes'] = np.concatenate(
                (self.buffer['outcomes'], data['outcomes']))[-self.buffer_len:]
            self.buffer['players'] = np.concatenate(
                (self.buffer['players'], data['players']))[-self.buffer_len:]

        print('Replay buffer length', self.buffer['boards'].shape[0])

    def sample_from_replay_buffer(self, samples):

        ind = np.random.randint(
            0, high=(len(self.buffer['boards'])-1), size=samples)
        data = {
            'boards': self.buffer['boards'][ind],
            'pi': self.buffer['pi'][ind],
            'outcomes': self.buffer['outcomes'][ind],
            'players': self.buffer['players'][ind]
        }
        return data

    def play_games_and_train(self,
                             num_games=100,
                             batch_size=1024,
                             num_evals=20,
                             win_thresh=0.6,
                             verbose=0,
                             epochs=3,
                             temp=1,
                             save_name=None):
        self.benchmark.mcts.temp = temp
        data = self.generate_games(num_games, verbose)
        self.add_to_replay_buffer(data)
        training_data = self.sample_from_replay_buffer(batch_size)
        self.train_challenger(training_data, epochs)
        win_prob = self.evaluate_challenger(num_evals, verbose)
        print('Challenger wins with probability', win_prob)

        if win_prob >= win_thresh:
            print(
                "Challenger outperformed benchmark, setting benchmark to challenger"
            )
            self.challenger.model.save('best_model.h5')
            # set the benchmark agent's model to the challenger's model
            benchmark_model = Model(self.size, self.input_moves,
                                    'best_model.h5')
            self.benchmark.model = benchmark_model
        else:
            print("Challenger cannot outperform benchmark")

        if save_name:
            self.save_data(data, save_name)

    def save_data(self, data, save_name):
        path = save_name
        print('Saving to', path)
        with open(path, "wb") as f:
            dill.dump(data, f)

    def train_challenger(self, data, epochs):
        ind = np.random.permutation(len(data['outcomes']))
        self.challenger.model.fit(data['boards'][ind], data['pi'][ind],
                                  data['outcomes'][ind], data['players'][ind],
                                  epochs)

    def evaluate_challenger(self, num_games, verbose):
        black_wins = 0
        selfplay = Selfplay(self.challenger, self.benchmark)
        print("Evaluating")
        for i in tqdm(range(num_games)):
            _, _, _, _, black_leads = selfplay.play_game(verbose=verbose)
            if black_leads == 0:
                black_wins += 0.5
            elif black_leads > 0:
                black_wins += 1

        return black_wins / num_games

    def generate_games(self, num_games, verbose):
        selfplay = Selfplay(self.benchmark, self.benchmark)
        boards_history = np.zeros((1, self.size, self.size))
        pi_history = np.zeros((1, self.size**2 + 1))
        outcome_history = np.array([])
        player_history = np.array([])

        print("Generating")
        for i in tqdm(range(num_games)):
            if verbose:
                print("Game", i)
            boards, pi, player, outcome, black_leads = selfplay.play_game(
                verbose=verbose)
            if verbose:
                print("Game ended, number of moves: ", len(pi))
                print()

            boards_history = np.vstack((boards_history, boards))
            pi_history = np.vstack((pi_history, pi))
            outcome_history = np.concatenate((outcome_history, outcome))
            player_history = np.concatenate((player_history, player))

        data = {
            'boards': boards_history[1:],  # first one is padding
            'pi': pi_history[1:],  # first one is padding
            'outcomes': outcome_history,
            'players': player_history
        }
        return data

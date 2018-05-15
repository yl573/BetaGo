from Shared.Consts import BLACK, WHITE
from .network import get_network, load_network
import numpy as np

class Model:

    def __init__(self, size, input_moves, saved_path=None):
        if saved_path:
            self.model = load_network(saved_path)
        else:
            self.model = get_network(input_moves, size)
        self.n_in = input_moves
        self.size = size

    def _reshape_input(self, input_boards, player):
        assert len(input_boards) == self.n_in

        dim = len(input_boards)*2+1
        out = np.zeros((1, dim, self.size, self.size))
        # need 4 dimensions due to Keras input requirement
        for i, move in enumerate(input_boards):
            black_stones = (move == 1).astype('float32')
            white_stones = (move == -1).astype('float32')
            if player == BLACK:
                out[0,2*i,:,:] = black_stones
                out[0,2*i+1,:,:] = white_stones
            else:
                out[0,2*i,:,:] = white_stones
                out[0,2*i+1,:,:] = black_stones
        if player == BLACK:
            out[0,-1,:,:] = np.ones(input_boards[0].shape)
        else:
            out[0,-1,:,:] = np.zeros(input_boards[0].shape)
        return out

    def format_board_history(self, boards, players):

        formatted = np.zeros((
            len(boards), 
            self.n_in*2+1,
            self.size, 
            self.size
        ))
        padding = np.zeros((self.n_in-1, self.size, self.size))
        boards = np.concatenate((padding, boards))
        for i in range(len(boards)-self.n_in):
            reshaped = self._reshape_input(boards[i:i+self.n_in], players[i])
            # print(reshaped.shape)
            formatted[i,:,:,:] = reshaped
        return formatted

    def save(self, file_path):
        self.model.save(file_path)

    def fit(self, boards, pi, outcomes, players, epochs):
        assert len(boards) == len(pi) == len(outcomes) == len(players)
        assert boards.shape[1] == boards.shape[2] == self.size

        import dill
        formatted_boards = self.format_board_history(boards, players)
        with open('formatted.pkl', "wb") as f:
            dill.dump(formatted_boards, f)

        self.model.fit(formatted_boards, [pi, outcomes], epochs=epochs)
                    
    def eval(self, boards, next_player):
        assert boards.shape[0] == self.n_in

        processed_boards = self._reshape_input(boards, next_player)
        pred = self.model.predict(processed_boards)

        policy = pred[0].reshape((-1))
        value = pred[1].reshape((-1))[0]

        return policy, value


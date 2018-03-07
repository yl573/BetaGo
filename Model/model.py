from Shared.Consts import BLACK, WHITE
from .network import get_network, load_network
import numpy as np

class Model:

    def __init__(self, size, input_moves, saved_path=None):
        if saved_path:
            self.model = load_network(saved_path)
        else:
            self.model = get_network(input_moves, size)
        self.input_moves = input_moves

    def _reshape_input(self, input_boards, next_player):
        dim = len(input_boards)*2+1
        out = np.zeros((1, dim, input_boards.shape[1], input_boards.shape[2]))
        for i, move in enumerate(input_boards):
            black_stones = (move == 1).astype('float32')
            white_stones = (move == -1).astype('float32')
            if next_player == BLACK:
                out[0,2*i,:,:] = black_stones
                out[0,2*i+1,:,:] = white_stones
            else:
                out[0,2*i,:,:] = white_stones
                out[0,2*i+1,:,:] = black_stones
        if next_player == BLACK:
            out[0,-1,:,:] = np.ones(input_boards[0].shape)
        else:
            out[0,-1,:,:] = np.zeros(input_boards[0].shape)
        return out

    def save(self, file_path):
        self.model.save(file_path)
                    
    def eval(self, boards, next_player):
        assert boards.shape[0] == self.input_moves

        processed_boards = self._reshape_input(boards, next_player)
        pred = self.model.predict(processed_boards)

        policy = pred[0].reshape((-1))
        value = pred[1].reshape((-1))[0]

        return policy, value


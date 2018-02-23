import GoBackend
import numpy as np

class Go:

    def __init__(self, N, black_first=True):
        GoBackend.set_size(N)
        self.N = N
        self.current_player = 'O' if black_first else 'X'
        self.board = GoBackend.Position.initial_state()

    def play(self, x, y):
        self.board = self.board.play_move(x*self.N+y, self.current_player)
        self._toggle_current_player()

    def get_legal_moves(self):
        legal = self.board.get_legal_moves()
        _, ko = self.board
        if ko is not None:
            legal[ko] = 0
        return np.array(legal).reshape((self.N,self.N))

    def print_board(self):
        print(self.board)
        print()

    def score(self):
        '''Black Score - White Score'''
        return self.board.score()

    def _toggle_current_player(self):
        if self.current_player == 'O':
            self.current_player = 'X'
        else:
            self.current_player = 'O'

# game = Go(5)
# game.play(0,2)
# game.play(0,0)
# game.play(1,2)
# game.play(0,1)
# game.play(1,1)
# game.play(1,0)
# game.play(2,0)
# game.play(1,0)
# game.play(0,0)
# game.play(2,1)
# game.play(4,4)
# game.play(3,0)
# game.play(4,3)
# game.play(1,0)
# game.play(3,3)
# game.play(2,4)
# game.play(2,0)


# print(game.get_legal_moves())

# game.print_board()
# print(game.score())



# pos.get_board()
# pos.score()





from . import GoBackend
import numpy as np
from Shared.Consts import WHITE, BLACK, EMPTY, num_to_char, char_to_num
from Shared.Functions import toggle_player

def board_to_string(board):
    l = board.shape[1]**2
    board_flat = board.reshape((l))
    board_str = ''.join(list((map(lambda x: num_to_char[x], board_flat))))
    return board_str

class GoSimulator:

    def __init__(self, N):
        GoBackend.set_size(N)
        self.N = N
        self.board = GoBackend.Position.initial_state()
        self.num_turns = 0
        self.num_passes = 0

    def set_board_from_prev_boards(self, prev_boards, next_player):
        prev = board_to_string(prev_boards[-2])
        curr = board_to_string(prev_boards[-1])
        ko = GoBackend.find_ko_from_boards(prev, curr)
        self.num_passes = int(prev == curr)
        self.num_turns = len(prev_boards)
        self.set_board(prev_boards[-1], next_player, ko=ko) 

    def set_board(self, board, next_player, ko=None):
        board_str = board_to_string(board)
        self.board = GoBackend.Position.set_board(board=board_str,ko=ko)
        self.current_player = next_player

    def play(self, x, y):
        self.board = self.board.play_move(y*self.N+x, self.current_player)
        self.current_player = toggle_player(self.current_player)
        self.num_turns += 1
        self.num_passes = 0
        end_condition = None
        if self.num_turns == self.N**2 * 2:
            end_condition = 'GAME OVER FROM TURN LIMIT REACHED (%s turns)' % self.num_turns
        return (self.as_array(), self.current_player, end_condition)

    def pass_move(self):
        self.board = self.board.pass_move()
        self.current_player = toggle_player(self.current_player)
        self.num_turns += 1
        self.num_passes += 1
        end_condition = None
        if self.num_passes == 2:
             end_condition = 'GAME OVER FROM 2 PASSES'
        return (self.as_array(), self.current_player, end_condition)

    def as_array(self):
        char_list = list(self.board.board)
        num_list = list(map(lambda x: char_to_num[x], char_list))
        board_array = np.array(num_list).reshape((self.N, self.N))
        return board_array

    def get_legal_moves(self):
        legal = self.board.get_legal_moves()
        return np.array(legal).reshape((self.N,self.N))

    def get_board(self):
        board = [ char_to_num[x] for x in self.board.board ]
        return np.array(board).reshape((self.N,self.N))

    def black_score_lead(self):
        '''Black Score - White Score'''
        return self.board.score()






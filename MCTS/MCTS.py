import numpy as np
from GoGame.GoSimulator import GoSimulator
from Shared.Consts import BLACK, WHITE
from Shared.Functions import toggle_player
import math

def calc_U(P, N, cpuct=1):
    N_sum = np.sum(N)
    return cpuct * P * np.sqrt(N_sum) / (1 + N)

def update_boards(boards, new_board):
    new_boards = np.delete(boards, 0, axis=0)
    new_board = np.array([new_board])
    return np.concatenate((new_boards, new_board))

def score_to_win_prob(last_player, black_lead):
    if black_lead == 0:
        return 0.5
    return 1 * (not (black_lead > 0) ^ (last_player == BLACK))

class MCTNode:

    def __init__(self, boards, P, V, player, is_end=False):
        self.boards = boards
        self.is_end = is_end
        self.V = V
        m, n, _ = boards.shape
        self.N = np.zeros(n**2+1)
        self.W = np.zeros(n**2+1)
        self.Q = np.zeros(n**2+1)
        self.P = P
        self.player = player
        self.children = {}

    def find_child(self, move):
        if str(move) in self.children:
            return self.children[str(move)]
        return None

    def add_child(self, move, child):
        self.children[str(move)] = child


class MCTS:
    def __init__(self, model, player, size, input_moves, start_boards=None):
        self.model = model
        self.game = GoSimulator(size)
        self.m = size
        self.n = size
        self.root = self._create_root(start_boards, player)

    def _create_root(self, start_boards, player):
        if start_boards is not None:
            boards = start_boards
        else:
            boards = np.zeros((self.m, self.n, self.n))
        P, V = self.model.eval(boards, player)
        return MCTNode(boards, P, V, player)

    def process_end_state(self, next_player):
        P = np.zeros(26)
        P[-1] = 1
        black_lead = self.game.black_score_lead()
        if black_lead == 0:
            V = 0.5
        elif next_player == BLACK:
            V = black_lead > 0
        else:
            V = black_lead < 0
        return P, V

    def _create_new_node(self, move):
        board, next_player, end = self._execute_move(move)
        new_boards = update_boards(self.root.boards, board)
        if end:
            P, V = self.process_end_state(next_player)
        else:
            P, V = self.model.eval(new_boards, next_player)
        return MCTNode(new_boards, P, V, next_player)

    def _execute_move(self, move):
        if move == self.n**2: # this is the pass move
            return self.game.pass_move()
        else:
            y, x = divmod(move, self.n)
            return self.game.play(x, y)

    def search_for_pi(self, iterations, temp=1, model=None):
        if model:
            self.model = model
        for i in range(iterations):
            self._search(self.root)
        pi = np.power(self.root.N, 1/temp) / np.sum(np.power(self.root.N, 1/temp))
        return pi

    def set_move(self, move):
        new_root = self.root.find_child(move)
        if new_root is None:   
            self.game.set_board_from_prev_boards(self.root.boards, self.root.player)  
            new_root = self._create_new_node(move)

        self.root = new_root

    def _search(self, node):
        self.game.set_board_from_prev_boards(node.boards, node.player)

        legal = self.game.get_legal_moves().flatten()
        legal = np.append(legal, 1)
        
        U = calc_U(node.P, node.N)
        score = (node.Q + U)
        if np.sum(score) == 0: 
            # if no moves have been played before
            # pick a random position
            score = np.random.uniform(size=(self.n**2+1))
        
        score[np.where(legal == 0)] = -np.inf
        move = np.argmax(score)

        assert legal[move] == 1

        child = node.find_child(move)
        if child is None:
            child = self._create_new_node(move)
            node.add_child(move, child)
            V = child.V
        elif child.is_end:
            V = child.V
        else:
            V = self._search(child)

        node.W[move] += V
        node.N[move] += 1
        node.Q[move] = node.W[move]/node.N[move]
        return V


import numpy as np
from GoGame.GoSimulator import GoSimulator
from Shared.Consts import BLACK, WHITE
from Shared.Functions import toggle_player
import math

def select_max(score):
    i = np.argmax(score)
    return i

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

    def __init__(self, boards, P, player):
        self.boards = boards
        self.m, self.n, _ = boards.shape
        self.N = np.zeros(self.n**2+1)
        self.W = np.zeros(self.n**2+1)
        self.Q = np.zeros(self.n**2+1)
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
    def __init__(self, model, player, m=8, n=5, start_boards=None):
        self.model = model
        self.game = GoSimulator(n)
        self.m = m
        self.n = n
        self.root = self._create_root(start_boards, player)

    def _create_root(self, start_boards, player):
        if start_boards is not None:
            boards = start_boards
        else:
            boards = np.zeros((self.m, self.n, self.n))
        P, _ = self.model.eval(boards)
        return MCTNode(boards, P, player)

    def search_for_pi(self, iterations=10, temp=1):
        for i in range(iterations):
            self._search(self.root)
        pi = np.power(self.root.N, 1/temp) / np.sum(np.power(self.root.N, 1/temp))
        return pi

    def set_move(self, move):
        new_root = self.root.find_child(move)
        if new_root is None:
            raise ValueError("Invalid move")
        self.root = new_root

    def _search(self, node):

        self.game.set_board_from_prev_boards(node.boards, node.player)
        legal = self.game.get_legal_moves().flatten()
        legal = np.append(legal, 1)

        # if there are no more positions to play
        if np.sum(legal) == 0:
            # evaluate who won
            return score_to_win_prob(toggle_player(node.player), self.game.black_score_lead())
        
        U = calc_U(node.P, node.N)
        score = (node.Q + U)
        if np.sum(score) == 0: 
            # if no moves have been played before
            # pick a random position
            score = np.random.uniform(size=(self.n**2+1))
        # add a negative score of -2 to illegal moves so that they will never be chosen 
        score = score - (1-legal)*2
        move = select_max(score)

        child = node.find_child(move)
        if child is not None:
            V = self._search(child)
        else:
            # print(self.game.board)
            # print(legal)
            # print(score * legal)
            # print(move)
            if move == self.n**2: # this is the pass move
                board, next_player = self.game.pass_move()
            else:
                x = move%self.n
                y = int(move/self.n)
                board, next_player = self.game.play(x, y)
                
            new_boards = update_boards(node.boards, board)
            P, V = self.model.eval(new_boards)
            child = MCTNode(new_boards, P, next_player)
            node.add_child(move, child)

        node.W[move] += V
        node.N[move] += 1
        node.Q[move] = node.W[move]/node.N[move]
        return V


import numpy as np
import math
from GoGame.GoSimulator import GoSimulator, board_to_string
from GoGame.GoBackend import find_move
from Shared.Consts import BLACK, WHITE
from Shared.Functions import toggle_player
from .Augment import eval_augment, reverse_P
from .Tree import print_tree


def update_boards(boards, new_board):
    new_boards = np.delete(boards, 0, axis=0)
    new_board = np.array([new_board])
    return np.concatenate((new_boards, new_board))


# def score_to_win_prob(last_player, black_lead):
#     if black_lead == 0:
#         return 0.5
#     return 1 * (not (black_lead > 0) ^ (last_player == BLACK))


class MCTNode:
    def __init__(self, boards, P, V, player, is_end=False):
        self.boards = boards
        self.is_end = is_end
        self.V = V
        m, n, _ = boards.shape
        self.N = np.zeros(n**2 + 1)
        self.W = np.zeros(n**2 + 1)
        self.Q = np.zeros(n**2 + 1)
        self.P = P
        self.player = player
        self.children = {}
        self.legal = get_legal(boards, player)

    def find_child(self, move):
        if str(move) in self.children:
            return self.children[str(move)]
        return None

    def add_child(self, move, child):
        self.children[str(move)] = child


game = GoSimulator(5)


def simulate_move(boards, player, move):
    game.set_board_from_prev_boards(boards, player)
    n = boards.shape[1]
    if move == n**2:  # this is the pass move
        return game.pass_move()
    else:
        y, x = divmod(move, n)
        return game.play(x, y)


def process_end_state(boards, player):
    game.set_board_from_prev_boards(boards, player)
    black_lead = game.black_score_lead()
    if black_lead == 0:
        V = 0
    elif player == BLACK:
        V = (black_lead > 0)*2 - 1
    else:
        V = (black_lead < 0)*2 - 1
    P = np.zeros(26)
    return P, V


def get_legal(boards, player):
    game.set_board_from_prev_boards(boards, player)
    legal = game.get_legal_moves().flatten()
    legal = np.append(legal, 1)
    return legal


def find_last_two_moves(boards):
    size = boards.shape[1]
    move1, _ = find_move(
        board_to_string(boards[-3]), board_to_string(boards[-2]))
    if move1 is None:
        move1 = size**2
    move2, _ = find_move(
        board_to_string(boards[-2]), board_to_string(boards[-1]))
    if move2 is None:
        move2 = size**2
    return move1, move2


class MCTS:
    def __init__(self, model, size, n_input, cpuct):
        self.model = model
        self.n_input = n_input
        self.size = size
        self.cpuct = cpuct
        self.root = None
        game = GoSimulator(self.size)

    def create_node(self, boards, player, end):
        if end:
            P, V = process_end_state(boards, player)
        else:
            augmented, rev_args = eval_augment(boards)
            aug_P, V = self.model.eval(augmented, player)
            P = reverse_P(aug_P, *rev_args)

        return MCTNode(boards, P, V, player)

    def print_tree(self):
        print_tree(self.root)

    def search_for_pi(self, boards, player, iterations, diri=False, temp=1):
        assert boards.shape[0] == self.n_input
        self.root = self.create_node(boards, player, False)

        # print(self.root.P)

        if diri:
            temp = 0.05
            alpha = tuple([0.03] * (self.size**2+1))
            nu = np.random.dirichlet(alpha)
            self.root.P = 0.75 * self.root.P + 0.25 * nu

        for i in range(iterations):
            self.search(self.root)

        exp = np.power(self.root.N, 1 / temp)
        pi = exp / np.sum(exp)
        # print('P', self.root.P)
        # print('V', self.root.V)
        # print('Q', self.root.Q)
        # print('Max Action Value',np.max(self.root.Q))
        return pi

    def search(self, node):
        U = self.cpuct * node.P * np.sqrt(np.sum(node.N)+1) / (1 + node.N)
        score = (node.Q + U)

        score[np.where(node.legal == 0)] = -np.inf
        move = np.argmax(score)

        assert node.legal[move] == 1
        child = node.find_child(move)
        if child is None:
            next_board, next_player, end = simulate_move(
                node.boards, node.player, move)
            next_board = np.reshape(next_board, (1, self.size, self.size))
            new_boards = np.vstack((node.boards[1:], next_board))
            child = self.create_node(new_boards, next_player, end)
            node.add_child(move, child)
            V = -child.V
        elif child.is_end:
            V = -child.V
        else:
            V = -self.search(child)

        # Note: the value is inverted because a good value for the opponent
        # is a bad value for the player

        node.W[move] += V
        node.N[move] += 1
        node.Q[move] = node.W[move] / node.N[move]
        return V

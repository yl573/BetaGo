import numpy as np
from GoGame.GoSimulator import GoSimulator
from Shared.Consts import BLACK, WHITE
from Shared.Functions import toggle_player
from Shared.GoState import GoState

class BoardArray():
    def __init__(self, np_arr):
        self.data = np_arr

    def __getitem__(self, pos):
        return self.data[pos[0]][pos[1]]

    def __setitem__(self, pos, value):
        self.self.data[pos[0]][pos[1]] = value

    def __repr__(self):
        return str(self.data)


class MCTNode:

    def _get_zeros(self):
        return BoardArray(np.zeros((self.N, self.N)))

    def __init__(self, board, P):
        self.board = board
        self.N = board.shape[0]
        self.N = self._get_zeros()
        self.W = self._get_zeros()
        self.Q = self._get_zeros()
        self.P = P
        self.children = {}

    def find_child(self, move):
        if str(move) in self.children:
            return self.children[str(move)]
        return None


def select_max(score):
    i = np.argmax(score)
    N = score.shape[0]
    return (int(i/N), i%N)

def search(node):
    U = None
    move = select_max(node.Q + U)
    child = node.find_child(move)
    if child is not None:
        V = search(child)
    else:
        game.set_board(node.board)
        board = game.play(*move)
        P, V = model.eval(board)
        node.children.append(MCTNode(board, P))


    node.W[move] += V
    node.N[move] += 1
    node.Q[move] = node.W[move]/node.N[move]
    return V

t = np.array([
    [1,0,0,0],
    [0,2,0,0],
    [0,0,3,0],
    [0,0,0,0]
])
# print(select_max(t))
root = MCTNode(t, )
game = GoSimulator()
search(t)


# class MCTS:
#     def __init__(self, start_states, model):
#         '''board_record has the last n board positions'''
#         self.N = start_states.shape[0]
#         self.game = GoSimulator()
#         self.model = model

#         self.pos_counts = np.zeros((self.N, self.N))
#         self.create_tree(start_states)
#         ko = GoSimulator.ko_from_boards(start_states[-2].board, start_states[-1].board)
#         self.game.set_board(start_states[-1].board, start_states[-1].player, ko=ko)

#     def create_tree(self, start_states):
#         self.root = MCTNode(start_states[0], None)
#         prev_node = self.root
#         for b in start_states[1:]:
#             new_node = MCTNode(b, prev_node)
#             prev_node.children.append(new_node)
#             prev_node = new_node

#     def _sample_board(self, board_prob):
#         rnd = np.random.uniform()
#         prob_flat = board_prob.flatten()
#         cumsum = np.cumsum(prob_flat)
#         index = len(cumsum) - len([p for p in cumsum if p > rnd])
#         N = board_prob.shape[0]
#         return (int(index / N), index % N)

#     def search(self, steps, n_past_moves=8):
#         for s in steps:
#             # need do record past few moves as well
#             past_moves = self.get_past_boards(n_past_moves)
#             prior, value = self.model.predict(past_moves)


#             prior *= self.game.board.get_legal_moves()
#             prior /= np.sum(prior)
#             move = self._sample_board(prior)
#             self.pos_counts[move[0]][move[1]] += 1

#             player, board = self.game.play(*move)
#             self.


# ini_board = np.array([[0, 0, 1, -1, 0], [0, 1, 1, -1, 0], [0, 1, -1, 0, -1],
#                       [1, 0, 1, -1, 0], [0, 0, 1, -1, 0]])
# # ini_board = np.array([
# #     [0,0,0,0,0],
# #     [0,0,0,0,0],
# #     [0,0,0,0,0],
# #     [0,0,0,0,0],
# #     [0,0,0,0,0]
# # ])

# ini_moves = [(2, 3)]


# class Model:
#     def predict(self, board):
#         return np.array([[0.1, 0.1], [0.4, 0.4]])

# model = Model()

# mcts = MCTS(ini_board, ini_moves, BLACK, model)
# mcts.search(10)

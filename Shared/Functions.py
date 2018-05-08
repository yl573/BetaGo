from Shared.Consts import BLACK, WHITE

def toggle_player(player):
    if player == BLACK:
        return WHITE
    return BLACK

def xy_to_index(x, y, N):
    return y*N+x

def index_to_xy(index, N):
    return index%N, int(index/N)

def board_to_string(board):
    l = board.shape[1]**2
    board_flat = board.reshape((l))
    board_str = ''.join(list((map(lambda x: num_to_char[x], board_flat))))
    return board_str
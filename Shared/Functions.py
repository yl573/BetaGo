from Shared.Consts import BLACK, WHITE

def toggle_player(player):
    if player == BLACK:
        return WHITE
    return BLACK

def xy_to_index(x, y, N):
    return y*N+x

def index_to_xy(index, N):
    return index%N, int(index/N)
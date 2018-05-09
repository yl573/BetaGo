from Shared.Consts import BLACK, WHITE

class writer :
    def __init__(self, file_name, old_stdout) :
        self.file_name = file_name
        with open(self.file_name, 'w') as f:
            f.write('Log\n\n')        
        self.old_stdout = old_stdout

    def write(self, text) :
        with open(self.file_name, 'a') as f:
            f.write(text)
        self.old_stdout.write(text)

    def flush(self):
        self.old_stdout.flush()

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
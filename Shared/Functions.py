from Shared.Consts import BLACK, WHITE
import os

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

def find_first_missing(in_array, start=1):
    '''
    input:  
        in_array(list): list of unordered integers
    output: 
        result (int):   value of first missing integer 
    '''
    
    array = sorted(set(in_array))
    
    if len(in_array)>len(array):
        print ("Warning: input array has non-unique numbers")
    if in_array[0]<0:
        print ("Warning: input array has negative numbers. "+
               "Returning first missing non-negative number")
        array = [num for num in array if num>0]
        
    
    offset=array[0]
    end = len(array)+offset

    if (start >= end):
        #print(1)
        return end
 
    if (start != array[start-offset]):
        #print (2)
        return start
 
    mid = int((start-offset + end)/ 2)

    # Left half has all elements
    # from 0 to mid
    if (array[mid-offset] == mid):
        #print (array[mid-offset])
        return find_first_missing(array, mid+1)
 
    return find_first_missing(array, start)
        
def check_int(string):
    try:
        integer = int(string)
        return True
    except:
        print ('Cannot convert "', string, " to string")
        return False
        
def create_unique_filename(directory, prefix='',
                           file_type=".pkl", underscore=True):
    '''
    Description:
        Creates unique numbered file name with the first missing 
        number for files inside the specified directory with the 
        specified prefix and file type, .
    Args:
        directory(string):  path to directory
        prefix(string):     Default value is ''. Prefix to attach
                            to file name.
        file_type(string):  Default value is '.pkl'. File types to
                            search for and save as.
        underscore(bool):   Default value is True. Option to set 
                            underscore between prefix and number
    Returns:
        new_name(string):   Unique numbered file name with specified
                            attributes from Args       
                            
    '''
    
    curr_filenames = ([name for name in os.listdir(directory) 
                       if os.path.isfile(os.path.join(directory, name))
                       and prefix in name and file_type in name])
    
    if underscore==True and len(prefix)>0:
        prefix = prefix+"_"
    curr_names = [names.replace(file_type,"") for names in curr_filenames]
    curr_names = [names.replace(prefix, "") for names in curr_names]
    curr_nums = ([int(num) for num in curr_names if check_int(num)])
    
    # Create number string
    if len(curr_nums)==0:
        new_num = 1
    else:
        new_num = find_first_missing(sorted(curr_nums))
    new_num = str(new_num)
    
    new_name = prefix+new_num+file_type
    return new_name

def specify_user(fn='user_info.txt'):
    try:
        with open(fn, 'r') as f:
            user = f.read()
        f.closed
        print ("Saving files under:    "+user)
    except IOError:
        print ("No user specified. Note that all game data is saved under user name")
        user = input("Please input name of user: ")
        with open(fn, 'w') as f:
            f.write(user)
        f.closed
    return user
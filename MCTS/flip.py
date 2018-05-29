# flips the board
import numpy as np
from random import randint

def flip(boards):
    flipped=np.transpose(boards,(0,2,1)) 
    return flipped

def rotate(boards,k):
    # 90 degree clockwise rotation k times
    rotated=np.rot90(boards,k=k,axes=(2,1))
    return rotated

boards=np.array(
    [[[1,2],[3,4]], 
    [[5,6],[7,8]]])

print(boards.shape)

print(flip(boards))
print(rotate(boards,1))

def augment(boards):
    # randomly flip and rotate
    toflip=randint(0,1)
    if toflip :
        boards=flip(boards)
    torotate=randint(0,3)
    boards=rotate(boards,toflip)
    return boards



# flips the board
import numpy as np
from random import randint

def to2D(arr):
    if len(arr.shape) == 2:
        return arr
    N = int(np.sqrt(len(arr)))
    return arr.reshape((N,N))  

def flip(boards, pi):
    flipped_boards = np.transpose(boards,(0,2,1)) 
    flipped_pi = np.array(pi)
    flipped_pi[:-1] = to2D(pi[:-1]).T.flatten()
    return flipped_boards, flipped_pi

def rotate(boards, pi ,k):
    # 90 degree clockwise rotation k times
    rotated_boards = np.rot90(boards,k=k,axes=(2,1))
    rotated_pi = np.array(pi)
    rotated_pi[:-1] = np.rot90(to2D(pi[:-1]), k=k, axes=(1,0)).flatten()
    return rotated_boards, rotated_pi

def augment(boards, pi):
    # randomly flip and rotate
    toflip = randint(0,1)
    if toflip :
        boards, pi = flip(boards, pi)
    k = randint(0,3)
    boards, pi = rotate(boards, pi, k)
    return boards, pi

def reverse_P(P, f, k):
    rev_P = np.array(P)
    rev_P_2D = to2D(rev_P[:-1])
    rev_P_2D = np.rot90(rev_P_2D,k=-k,axes=(1,0))
    if f:
        rev_P_2D = np.transpose(rev_P_2D,(1,0)) 
    rev_P[:-1] = rev_P_2D.flatten()
    return rev_P

def eval_augment(arr):
    f = randint(0,1)
    k = randint(0,3)
    aug = np.array(arr)
    if f:
        aug = np.transpose(aug,(0,2,1)) 
    aug = np.rot90(aug,k=k,axes=(2,1))
    return aug, (f, k)

def augment_dataset(dataset):
    # 8x the dataset with augmentation
    augmented = np.array(dataset[0])
    for i in range(len(dataset)):
        for k in range(4):
            rotated_boards, rotated_pi = rotate(dataset[i][0], dataset[i][1], k)
            flipped_boards, flipped_pi = flip(rotated_boards, rotated_pi) 
            rotated_data = [rotated_boards, rotated_pi, dataset[i][2], dataset[i][3]] 
            flipped_data = [flipped_boards, flipped_pi, dataset[i][2], dataset[i][3]] 
            augmented = np.vstack((augmented, rotated_data))
            augmented = np.vstack((augmented, flipped_data))

    return augmented[1:]

# boards=np.array(
#     [[[1,2],[3,4]], 
#     [[5,6],[7,8]]])

# aug, rev = eval_augment(boards)
# print(boards)
# print(aug)
# print(rev(aug))

# pi=np.array(
#     [1,2,3,4,5]
# )


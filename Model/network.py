
import numpy as np
# np.random.seed(123)  # for reproducibility
import keras
from keras.models import load_model
from keras import backend as K
from keras.models import Sequential, Model
from keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D, Lambda, Add, Input, Subtract
from keras.layers.normalization import BatchNormalization
from keras.utils import np_utils
from keras import regularizers
from keras.datasets import mnist

reg = regularizers.l2(1e-4)

def residual_block(y):
    shortcut = y

    y = Conv2D(32, kernel_size=(3, 3), strides=(1, 1), padding='same', kernel_regularizer=reg)(y)
    y = BatchNormalization()(y)
    y = Activation('relu')(y)

    y = Conv2D(32, kernel_size=(3, 3), strides=(1, 1), padding='same', kernel_regularizer=reg)(y)
    y = BatchNormalization()(y)

    y = keras.layers.add([shortcut, y])
    y = Activation('relu')(y)

    return y

def policy_loss(y_true, y_pred):
    return -K.sum(y_true * K.log(y_pred))

def load_network(file_path):
    return load_model(file_path, custom_objects={'policy_loss': policy_loss})


def get_network(input_moves, N):
    # this is the actual model for BetaGo
    inp = Input((2*input_moves+1,N,N))

    # input convolution
    y = Conv2D(32, (3, 3), padding='same', kernel_regularizer=reg)(inp)
    y = BatchNormalization()(y)
    y = Activation('relu')(y)
    # residual blocks
    y = residual_block(y)
    y = residual_block(y)
    y = residual_block(y)
    y = residual_block(y)
    y = residual_block(y)

    # policy
    y_policy = Conv2D(2, (1, 1), kernel_regularizer=reg)(y)
    y_policy = BatchNormalization()(y_policy)
    y_policy = Flatten()(y_policy)
    y_policy = Activation('relu')(y_policy)
    policy_out = Dense(N**2+1, activation='softmax', name='policyout', kernel_regularizer=reg)(y_policy)

    # value
    y_value = Conv2D(1, (1, 1), kernel_regularizer=reg)(y)
    y_value = BatchNormalization()(y_value)
    y_value = Flatten()(y_value)
    y_value = Activation('relu')(y_value)
    y_value = Dense(64, activation='relu', kernel_regularizer=reg)(y_value)
    value_out = Dense(1, activation='tanh', name='valueout', kernel_regularizer=reg)(y_value)

    model = Model(inp, [policy_out,value_out])
    model.compile(loss=[policy_loss, 'mse'], optimizer='adam')
    return model

# class TestModel:
#     def predict(self, board):
#         P = np.ones(26)/26
#         V = np.array([0.1])
#         return P, V





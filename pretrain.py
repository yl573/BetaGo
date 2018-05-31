
import dill
import os
import numpy as np
from MCTS.Augment import augment_dataset
from Shared.Consts import BLACK, WHITE

folder = "game_data"
files = os.listdir(folder)
print(files)

buffer = None

for file_name in files:
    if file_name[-4:] != '.pkl':
        continue
    path = folder+'/'+file_name
    print('Loading', path)
    with open(path, "rb") as f:
        data = dill.load(f)
        if not buffer:
            buffer = data
        else:
            buffer = np.vstack((buffer, data))

augmented = augment_dataset(buffer[20:21])

from Model import Model

model = Model(5, 4, None)
model.fit(augmented, 10)
model.save('test.h5')
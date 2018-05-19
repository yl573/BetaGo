
from Model import Model
import dill
import os
import numpy as np

model = Model(5, 4, None)

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
            buffer['boards'] = np.vstack(
                (buffer['boards'], data['boards']))
            buffer['pi'] = np.vstack((buffer['pi'],
                                           data['pi']))
            buffer['outcomes'] = np.concatenate(
                (buffer['outcomes'], data['outcomes']))
            buffer['players'] = np.concatenate(
                (buffer['players'], data['players']))

model.fit(buffer['boards'], buffer['pi'],
            buffer['outcomes'], buffer['players'], 10)

model.save('pretrain.h5')
from Training import Trainer
from Shared.Functions import writer, create_unique_filename, specify_user
import sys
import os
import time

# Default paths. Change as needed
MODEL_DIR = 'Trained_Models'
BENCHMARK = 'michael_best_040618.h5'
INIT_MODEL  = 'michael_best_040618.h5'
SAVE_DIR = 'game_data'
# Constants. Change as needed
NUM_GAMES = 1
NUM_EVALS = 20
NUM_ITER = 3

sys.stdout = writer('train.log', sys.stdout)

if not os.path.exists(SAVE_DIR):
    print (SAVE_DIR+" does not exist. Making new directory")
else:
    print (SAVE_DIR+" exists. Saving training data in this directory")
os.makedirs(SAVE_DIR, exist_ok=True)

trainer = Trainer(
    model_file=os.path.join(MODEL_DIR, INIT_DIR), 
    benchmark_file=os.path.join(MODEL_DIR, BENCHMARK),
    search_iters=110, 
    buffer_len=16384,
    cpuct=1
)

user = specify_user(fn="user_info.txt")

for i in range(NUM_ITER):
    timestamp = time.strftime('%d%m%y')
    save_filename = create_unique_filename(SAVE_DIR, user+'_'+timestamp, file_type='.pkl')
    print ("Saving as ", save_filename)
    
    trainer.play_games_and_train(
        num_games=NUM_GAMES,
        batch_size=4098, 
        num_evals=NUM_EVALS,
        win_thresh=0.7, 
        verbose=0, 
        epochs=3, 
        save_name=os.path.join(SAVE_DIR, save_filename)
    )
    trainer.challenger.model.save('checkpoint.h5')



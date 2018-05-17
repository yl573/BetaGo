from Training import Trainer
from Shared.Functions import writer
import sys

sys.stdout = writer('train.log', sys.stdout)

trainer = Trainer(
    model_file='best_model.h5', 
    benchmark_file='best_model.h5',
    search_iters=110, 
    buffer_len=4096,
    cpuct=1
)

for i in range(10):
    trainer.play_games_and_train(
        num_games=1,
        batch_size=1, 
        num_evals=1,
        win_thresh=0.65, 
        verbose=1, 
        epochs=1, 
        save_name=None#'game_data/data_16_3_' + str(i) + '.pkl'
    )
    trainer.challenger.model.save('checkpoint.h5')



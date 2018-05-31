from Training import Trainer
from Shared.Functions import writer
import sys

sys.stdout = writer('train.log', sys.stdout)

trainer = Trainer(
    model_file='pretrain_21.h5', 
    benchmark_file='pretrain_21.h5',
    search_iters=110, 
    buffer_len=16384,
    cpuct=1
)

for i in range(2):
    trainer.play_games_and_train(
        num_games=1,
        batch_size=4098, 
        num_evals=1,
        win_thresh=0.7, 
        verbose=0, 
        epochs=3, 
        save_name='game_data/' + str(i) + '.pkl'
    )
    trainer.challenger.model.save('checkpoint.h5')



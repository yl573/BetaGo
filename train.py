from Training import Trainer
from Shared.Functions import writer
import sys

sys.stdout = writer('train.log', sys.stdout)

trainer = Trainer(
    model_file=None, 
    benchmark_file=None,
    search_iters=110, 
    buffer_len=4096,
    cpuct=1
)

for i in range(10):
    trainer.play_games_and_train(
        num_games=1,
        batch_size=4096, 
        num_evals=1,
        win_thresh=0.65, 
        verbose=0, 
        epochs=5, 
        temp=0.5,
        save_name='game_data/edward_19_' + str(i) + '.pkl'
    )
    trainer.challenger.model.save('checkpoint.h5')



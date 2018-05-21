from Training import Trainer
from Shared.Functions import writer
import sys

sys.stdout = writer('train.log', sys.stdout)

trainer = Trainer(
    model_file='best_model.h5', 
    benchmark_file='best_model.h5',
    search_iters=110, 
    buffer_len=16384,
    cpuct=1,
    init_buffer=[
        'game_data/edward_21_2.pkl',
        'game_data/edward_21_3.pkl',
        'game_data/edward_21_4.pkl',
        'game_data/edward_21_5.pkl',
        'game_data/edward_21_6.pkl',
        'game_data/edward_21_7.pkl',
        'game_data/edward_21_8.pkl'
    ]
)

for i in range(10):
    trainer.play_games_and_train(
        num_games=50,
        batch_size=4098, 
        num_evals=20,
        win_thresh=0.7, 
        verbose=0, 
        epochs=1, 
        save_name='game_data/edward_21_' + str(i+6) + '.pkl'
    )
    trainer.challenger.model.save('checkpoint.h5')



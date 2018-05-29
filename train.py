from Training import Trainer
from Shared.Functions import writer
import sys

sys.stdout = writer('train.log', sys.stdout)

trainer = Trainer(
    model_file='pretrain_21.h5', 
    benchmark_file='pretrain_21.h5',
    search_iters=110, 
    buffer_len=16384,
    cpuct=1,
    init_buffer=[
        'game_data/andrew_20_0.pkl',
        'game_data/andrew_20_1.pkl',
        'game_data/andrew_20_2.pkl',
        'game_data/andrew_20_3.pkl',
        'game_data/andrew_20_4.pkl',
        'game_data/andrew_20_5.pkl',
        'game_data/andrew_20_6.pkl'
    ]
)

for i in range(10):
    trainer.play_games_and_train(
        num_games=100,
        batch_size=4098, 
        num_evals=20,
        win_thresh=0.7, 
        verbose=0, 
        epochs=3, 
        save_name='game_data/andrew_22_' + str(i+6) + '.pkl'
    )
    trainer.challenger.model.save('checkpoint.h5')



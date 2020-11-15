from Source.InformatiCupGame.GameWrapper import GameWrapper
from Source.Main.RandomPlayer import RandomPlayer
from Source.Main.PassivePlayer import PassivePlayer
from Source.Main.HeuristicPlayer import HeuristicPlayer
import time

start = time.time()

winners = [0, 0, 0, 0, 0, 0, 0]
round_counter = 0
game_count = 100

for i in range(game_count):
    game_wrapper = GameWrapper(70, 70, [RandomPlayer(i+1) for i in range(6)])
    winner = game_wrapper.get_winner()
    round_counter += game_wrapper.get_round_counter()
    winners[winner] = winners[winner] + 1

print((time.time() - start)/60)
print(str(winners))
print('Average Game Length: ', str(round_counter/game_count))

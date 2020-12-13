from Source.InformatiCupGame.GameWrapper import GameWrapper
from Source.Main.RandomPlayer import RandomPlayer
from Source.Main.PassivePlayer import PassivePlayer
from Source.Main.HeuristicPlayer import HeuristicPlayer
import time

start = time.time()

winners = [0, 0, 0, 0, 0, 0, 0]
round_counter = 0
game_count = 50

for i in range(game_count):
    game_wrapper = GameWrapper(70, 70, [HeuristicPlayer(1, [1, 1, 1]), HeuristicPlayer(2, [1, 1, 1]), HeuristicPlayer(3, [1, 1, 1]), HeuristicPlayer(4, [1, 1, 1]), HeuristicPlayer(5, [1, 1, 1]), HeuristicPlayer(6, [1, 1, 1])])
    winner = game_wrapper.get_winner()
    round_counter += game_wrapper.get_round_counter()
    winners[winner] = winners[winner] + 1

print((time.time() - start)/60)
print(str(winners))
print('Average Game Length: ', str(round_counter/game_count))

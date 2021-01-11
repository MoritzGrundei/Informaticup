from Source.InformatiCupGame.GameWrapper import GameWrapper
from Source.Main.RandomPlayer import RandomPlayer
from Source.Main.PassivePlayer import PassivePlayer
from Source.Main.HeuristicPlayer import HeuristicPlayer
from Source.Main.PathFindingPlayer import PathFindingPlayer
from Source.Main.SimplePlayer import SimplePlayer

import time

start = time.time()

winners = [0, 0, 0, 0, 0, 0, 0]
round_counter = 0
game_count = 500
try:
    for i in range(game_count):
        game_wrapper = GameWrapper(70, 70, [HeuristicPlayer(1, [1, 1, 1],49), HeuristicPlayer(2, [1, 1, 1], 59), SimplePlayer(49), SimplePlayer(59), PathFindingPlayer(9, 49), PathFindingPlayer(9, 59)])
        winner = game_wrapper.get_winner()
        round_counter += game_wrapper.get_round_counter()
        winners[winner] = winners[winner] + 1
finally:
    print((time.time() - start)/60)
    print(str(winners))
    print('Average Game Length: ', str(round_counter/game_count))

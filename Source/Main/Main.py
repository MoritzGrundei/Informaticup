from Source.InformatiCupGame.GameWrapper import GameWrapper
from Source.Main.TestPlayer import TestPlayer
import time

start = time.time()

winners = [0, 0, 0, 0, 0, 0, 0]


for i in range(1):
    winner = GameWrapper(50, 50, [TestPlayer(i+1) for i in range(6)]).get_winner()
    winners[winner] = winners[winner] + 1

print((time.time() - start)/60)
print(str(winners))

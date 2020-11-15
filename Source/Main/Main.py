from Source.InformatiCupGame.GameWrapper import GameWrapper
from Source.Main.TestPlayer import TestPlayer
from Source.Main.PassivePlayer import PassivePlayer
import time

start = time.time()

winners = [0, 0, 0, 0, 0, 0, 0]


for i in range(3000):
    winner = GameWrapper(70, 70, [PassivePlayer(i+1) for i in range(6)]).get_winner()
    winners[winner] = winners[winner] + 1

print((time.time() - start)/60)
print(str(winners))

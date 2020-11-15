from Source.InformatiCupGame.GameWrapper import GameWrapper
from Source.Main.TestPlayer import TestPlayer
from Source.Main.PassivePlayer import PassivePlayer
from Source.Main.SecondTry import SecondTry
import time

start = time.time()

winners = [0, 0, 0, 0, 0, 0, 0]


for i in range(1):
    winner = GameWrapper(10, 10, [SecondTry(i+1) for i in range(6)]).get_winner()
    winners[winner] = winners[winner] + 1

print((time.time() - start)/60)
print(str(winners))

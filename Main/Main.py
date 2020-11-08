from InformatiCupGame import GameWrapper
from TestPlayer import TestPlayer


GameWrapper(10, 10, [TestPlayer(i+1) for i in range(6)])
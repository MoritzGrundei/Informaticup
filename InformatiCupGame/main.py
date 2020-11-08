from Game import Game
from PlayerTest import PlayerTest
import time

class GameWrapper:
    def __init__(self):
        self.game = Game(10, 10, time.time())
        self.players = []
        for i in range(6):
            player = PlayerTest()
            self.players.append(player)
        self.run()

    def run(self):
        self.game.print_game_state()
        print(self.game.running)
        while self.game.running:
            inputs = []
            for player in self.players:
                inputs.append(player.get_command())
            self.game.tick(inputs)
            self.game.print_game_state()
        self.game.plot_field()

GameWrapper()

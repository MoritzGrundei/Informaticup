from Game import Game
from PlayerTest import PlayerTest
import time

class GameWrapper:
    def __init__(self):
        self.player_count = 6
        self.game = Game(10, 10, self.player_count, time.time())
        self.players = []
        for i in range(self.player_count):
            player = PlayerTest(i+1, self)
            self.players.append(player)
        self.run()

    def run(self):
        print(self.get_game_state(1))
        print(self.game.running)
        while self.game.running:
            inputs = []
            for player in self.players:
                inputs.append(player.get_command())
                print(player.get_player_game_state())
            self.game.tick(inputs)
        self.game.plot_field()

    def get_game_state(self, id):
        return self.game.return_game_state(id)

GameWrapper()
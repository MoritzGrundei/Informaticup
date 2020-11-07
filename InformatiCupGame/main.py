from Game import Game
import time

game = Game(50, 50, time.time())
game.print_game_state()
print(game.running)
while game.running:
    game.tick()
    game.print_game_state()
game.plot_field()
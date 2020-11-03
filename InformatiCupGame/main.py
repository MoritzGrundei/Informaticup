from Game import Game

game = Game(50, 50)
game.print_game_state()
print(game.running)
while game.running:
    game.tick()
    game.print_game_state()
game.plot_field()
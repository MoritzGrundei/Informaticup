from InformatiCupGame.Game import Game

game = Game(20, 20)
game.print_game_state()
print(game.running)
while game.running:
    game.tick()
    game.print_game_state()




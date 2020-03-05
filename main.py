from game_main import Game

game = Game()
game.set_map("default_map.txt")
game.enable_fog()
game.enable_explorer()
game.run()


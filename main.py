# from game_main import Game

# game = Game()
# game.set_map("default_map.txt")
# game.enable_fog()
# #game.enable_explorer()
# game.enable_ai()
# game.init_thorpy()
# game.run()

from game_GOAP import Game
import game_time as time

game = Game()
game.set_map("default_map.txt")
game.set_fog_visibility(False)
game.enable_GOAP_ai()
game.run()




    
    






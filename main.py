# from game_main import Game

# game = Game()
# game.set_map("default_map.txt")
# # game.enable_fog()
# # game.enable_explorer()
# game.enable_ai()
# game.init_thorpy()
# game.run()

# from game_GOAP import Game as GOAP_GAME

# gg = GOAP_GAME()
# gg.set_map("default_map.txt")
# gg.set_fog_visibility(False)
# gg.enable_GOAP_ai()
# #gg.enable_dragon_scenario()
# gg.run()

from GOAP2.game import Game as MegaOwo

owo = MegaOwo()
owo.set_map("default_map.txt")
owo.set_fog_visibility(False)
owo.run()
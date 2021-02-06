# from game_main import Game

# game = Game()
# game.set_map("default_map.txt")
# game.enable_fog()
# #game.enable_explorer()
# game.enable_ai()
# game.init_thorpy()
# game.run()

import game_time as time
import GOAP.agent as agent
import GOAP.Agents.dragon_keeper as dragon_keeper

#agent = agent.GOAPAgent()
dk = dragon_keeper.DragonKeeper()
dk.start()


while True:

    time.clock.update(3)

    dk.update()






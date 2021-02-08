# from game_main import Game

# game = Game()
# game.set_map("default_map.txt")
# game.enable_fog()
# #game.enable_explorer()
# game.enable_ai()
# game.init_thorpy()
# game.run()

import game_time as time

from GOAP.Agents.dragon_keeper import DragonKeeper
from GOAP.Agents.dragon import Dragon
from GOAP.Agents.miner import Miner

dragon = Dragon()

agents = []
agents.append(DragonKeeper(dragon))
agents.append(dragon)
#agents.append(Miner())

for agent in agents:
    agent.start()

while True:

    time.clock.update(60)

    for agent in agents:
        agent.update()
    
    






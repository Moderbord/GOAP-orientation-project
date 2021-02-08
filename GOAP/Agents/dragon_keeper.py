from GOAP.Agents.labourer import Labourer
from GOAP.action_set import ActionSet

# Actions
from GOAP.Actions.fish_for_dragon import FishForDragon
from GOAP.Actions.hunt_for_dragon import HuntForDragon
from GOAP.Actions.feed_dragon import FeedDragon

class DragonKeeper(Labourer):

    def __init__(self, dragon):
        super().__init__()

        # local variables
        self.dragon = dragon

        # actions
        self.add_action(FishForDragon())
        self.add_action(HuntForDragon())
        self.add_action(FeedDragon())

    def get_world_state(self):
        # Returns an evaluated set of the world state
        world_data = {}
        #
        world_data["dragonIsHungry"] = self.dragon.get_world_state()["isHungry"]
        world_data["hasMeat"] = self.backpack.count("Meat") > 0
        #
        return world_data

    def create_goal_state(self):
        goal_state = ActionSet()
        goal_state.add("satisfyDragon", True)

        return goal_state

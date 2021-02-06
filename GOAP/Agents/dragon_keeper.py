import GOAP.Actions.mine_ore as mine_ore
import GOAP.Agents.labourer as labourer
import GOAP.action_set as action_set

class DragonKeeper(labourer.Labourer):

    def __init__(self):
        super().__init__()
        self.add_action(mine_ore.MineOre())

    def create_goal_state(self):
        goal_state = action_set.ActionSet()

        goal_state.add("collectOre", True)
        return goal_state

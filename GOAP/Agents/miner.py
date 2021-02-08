from GOAP.Agents.labourer import Labourer
from GOAP.action_set import ActionSet

# Actions
from GOAP.Actions.mine_ore import MineOre
from GOAP.Actions.deliver_ore import DeliverOre

class Miner(Labourer):

    def __init__(self):
        super().__init__()
        self.add_action(MineOre())
        self.add_action(DeliverOre())

    def create_goal_state(self):
        goal_state = ActionSet()
        goal_state.add("collectOre", True)
        
        return goal_state

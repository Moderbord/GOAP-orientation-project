import game_entities as entities
import message_dispatcher as dispatcher
import entity_state

class AIGlobalState(entity_state.State):
    def enter(self, player):
        pass

    def execute(self, player):
        pass

    def exit(self, player):
        pass

    def on_message(self, player, message):
        pass
        # catch info about discovered tiles here

class AIStateIdle(entity_state.State):
    def enter(self, player):
        pass

    def execute(self, player):
        pass

    def exit(self, player):
        pass

    def on_message(self, player, message):
        pass

class AIStateExplore(entity_state.State):
    def enter(self, player):
        self.explorers = []
        for unit in player.unit_list:
            if isinstance(unit, entities.UnitExplorer):
                self.explorers.append(unit)

    def execute(self, player):
        for explorer in self.explorers:
            if not explorer.is_traversing and explorer.is_visible:
                explorer.fsm.change_state(entity_state.StateExplore())

    def exit(self, player):
        pass

    def on_message(self, player, message):
        if message.msg == dispatcher.MSG.NewExplorerUnit:
            # add new explorer to explorer list when approriate message is recieved
            self.explorers.append(message.sender)
            return True

        return False
        
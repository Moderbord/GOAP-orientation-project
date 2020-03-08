import game_entities as entities
import message_dispatcher as dispatcher
import entity_state

class AIGlobalState(entity_state.State):
    def Enter(self, player):
        pass

    def Execute(self, player):
        pass

    def Exit(self, player):
        pass

    def OnMessage(self, player, message):
        pass
        # catch info about discovered tiles here

class AIStateIdle(entity_state.State):
    def Enter(self, player):
        pass

    def Execute(self, player):
        pass

    def Exit(self, player):
        pass

    def OnMessage(self, player, message):
        pass

class AIStateExplore(entity_state.State):
    def Enter(self, player):
        self.explorers = []
        for unit in player.unit_list:
            if isinstance(unit, entities.UnitExplorer):
                self.explorers.append(unit)

    def Execute(self, player):
        for explorer in self.explorers:
            if not explorer.is_traversing:
                explorer.fsm.ChangeState(entity_state.StateExplore())

    def Exit(self, player):
        pass

    def OnMessage(self, player, message):
        if message.msg == dispatcher.MSG.NewExplorerUnit:
            self.explorers.append(message.sender)
        # add new explorer to explorer list when approriate message is recieved
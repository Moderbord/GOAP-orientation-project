import game_entities as entities
import message_dispatcher as dispatcher
import game_time as time
import entity_state

class AIGlobalState(entity_state.State):
    def enter(self, player):
        pass

    def execute(self, player):
        if player.time_since_lask_task_update >= 15:
            player.update_task_list()
            player.time_since_lask_task_update = 0
        player.time_since_lask_task_update += time.delta_time

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

class AIStateGather(entity_state.State):
    def enter(self, player):
        self.workers = []
        for unit in player.unit_list:
            if isinstance(unit, entities.UnitWorker) and unit.fsm.is_in_state(entity_state.StateIdle):
                self.workers.append(unit)

        # has no free workers
        if not self.workers:
            player.prepend_goal(["Unit", "Worker", 1])

    def execute(self, player):
        for worker in self.workers:
            if not worker.is_traversing and worker.fsm.is_in_state(entity_state.StateIdle):
                worker.fsm.change_state(entity_state.StateGather())

    def exit(self, player):
        pass

    def on_message(self, player, message):
        if message.msg == dispatcher.MSG.NewWorkerUnit:
            # add new explorer to explorer list when approriate message is recieved
            self.workers.append(message.sender)
            return True

        return False

class AIStateExplore(entity_state.State):
    def enter(self, player):
        self.explorers = []
        for unit in player.unit_list:
            if isinstance(unit, entities.UnitExplorer):
                self.explorers.append(unit)
        
        # has no explorers
        if not self.explorers:
            player.prepend_goal(["Unit", "Explorer", 3])

    def execute(self, player):
        for explorer in self.explorers:
            if not explorer.is_traversing and explorer.fsm.is_in_state(entity_state.StateIdle):
                explorer.fsm.change_state(entity_state.StateExplore())

    def exit(self, player):
        pass

    def on_message(self, player, message):
        if message.msg == dispatcher.MSG.NewExplorerUnit:
            # add new explorer to explorer list when approriate message is recieved
            self.explorers.append(message.sender)
            return True

        return False
        
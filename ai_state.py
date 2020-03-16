import game_entities as entities
import message_dispatcher as dispatcher
import game_time as time
import entity_state

class AIGlobalState(entity_state.State):
    def enter(self, player):
        pass

    def execute(self, player):
        if player.time_since_lask_task_update >= 1000:
            #player.update_task_list()
            player.time_since_lask_task_update = 0
        player.time_since_lask_task_update += time.delta_time

    def exit(self, player):
        pass

    def on_message(self, player, message):
        #player.entity_list.append(message.sender)
        # if message.msg == dispatcher.MSG.NewWorkerUnit:
        #     player.worker_units.append(message.sender)
        #     return True
        
        # if message.msg == dispatcher.MSG.NewExplorerUnit:
        #     player.explorer_units.append(message.sender)
        #     return True

        # if message.msg == dispatcher.MSG.NewArtisanUnit:
        #     player.artisan_units.append(message.sender)
        #     return True

        # if message.msg == dispatcher.MSG.NewSoldierUnit:
        #     player.soldier_units.append(message.sender)
        #     return True

        return False

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
        self.update_interval = 1
        self.time_since_last_update = 0

    def execute(self, player):
        if self.time_since_last_update >= self.update_interval:
            # count current workers that is currently gathering
            count = 0
            for worker in player.entities_where(lambda e: isinstance(e, entities.UnitWorker)):
                if worker.fsm.is_in_state(entity_state.StateGather):
                    count += 1
            # try to have x workers in gathering state at the same time (currently 10)
            new_workers = player.get_available_units(entities.UnitWorker, 10 - count)
            for worker in new_workers:
                worker.fsm.change_state(entity_state.StateGather())
            # if count is less want wanted -> queue work
            if count < 10:
                player.prepend_goal(["Unit", "Worker", 10])
            # reset timer   
            self.time_since_last_update = 0

        self.time_since_last_update += time.delta_time

    def exit(self, player):
        pass

    def on_message(self, player, message):
        pass

class AIStateExplore(entity_state.State):
    def enter(self, player):
        self.update_interval = 1
        self.time_since_last_update = 0

    def execute(self, player):
        if self.time_since_last_update >= self.update_interval:
            # count current explorers
            count = 0
            for explorer in player.entities_where(lambda e: isinstance(e, entities.UnitExplorer)):
                # if explorer is not currently exploring -> change its state
                if explorer.is_idle:
                    explorer.fsm.change_state(entity_state.StateExplore())
                count += 1
            # try to have x amount of explorers units (currently 5)
            if count < 5:
                player.prepend_goal(["Unit", "Explorer", 5])
            # reset timer   
            self.time_since_last_update = 0

        self.time_since_last_update += time.delta_time

    def exit(self, player):
        pass

    def on_message(self, player, message):
        pass
        
from zootopia.core.logger import logger
from zootopia.controller.context import ContextManager
from zootopia.controller.intent import IntentManager
from zootopia.controller.action import ActionManager
from zootopia.controller.memory import ShortTermHistory, GeneralMemory
from zootopia.core.schema import ActionType


class AgentController:
    def __init__(
        self, 
        context: ContextManager
    ) -> None:
        self.context = context
        self.intent = IntentManager(context)
        self.action = ActionManager(context)
        self.short_term_history = ShortTermHistory(context)
        self.general_memory = GeneralMemory(context)

    def handle_message(self):
        try:
            recent_messages = self.short_term_history.get_recent_messages(count=10)
            possible_actions = [
                ActionType.MESSAGE,
                ActionType.RECALL,
                ActionType.WEB_SEARCH,
            ]

            # Produce list of actions based on recent messages
            actions = self.intent.produce_actions(recent_messages, possible_actions)
            
            # Execute the actions
            results = self.action.execute_actions(actions)
            
            # Update general memory with the results
            self.general_memory.update_memory(results)
            
            # Store new memories if necessary
            self.general_memory.store_memory(recent_messages[-1])
            
            # Handle any necessary responses or side effects
            self._handle_results(results)
            
        except Exception as e:
            logger.error(f"Error in handling message: {str(e)}")

    def _handle_results(self, results):
        # Implement logic to handle the results of actions
        # This could involve sending messages, updating application state, etc.
        pass
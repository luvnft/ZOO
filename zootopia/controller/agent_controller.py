from zootopia.core.utils.logger import logger
from zootopia.controller.context.context import ContextManager
from zootopia.controller.intent.intent import IntentManager
from zootopia.controller.action.action import ActionManager
from zootopia.controller.memory.memory import MemoryManager



class AgentController:
    def __init__(
        self, context: ContextManager
    ) -> None:
        self.context = context
        self.intent = IntentManager(context)
        self.action = ActionManager(context)
        self.memory = MemoryManager(context)

    # TODO: design and implement pseudo-code
    def handle_message(self):
        message_history = self.memory.get_message_history()
        actions = self.intent.produce_actions(message_history, )
        results = self.action.execute_actions(actions)
        self.memory.update_memory(results)


from src.langgraphagenticai.state.state import State

class BasicChatbotNode:
    """
    Docstring for BasicChatbotNode
    """
    def __init__(self,model):
        self.llm = model 

    def process(self, state: State) -> dict:
        """
        Process state messages through LLM

        :param state: State object containing messages
        :type state: State
        :return: Dict with LLM responses
        :rtype: dict
        """

        messages_text = []
        for msg in state['messages']:

            if hasattr(msg, 'content'):
                messages_text.append(msg.content)
            else:
                messages_text.append(str(msg))

        response = self.llm.invoke(messages_text)

        return {"messages": response}
from src.langgraphagenticai.state.state import State

class BasicChatbotNode:
    """
    Docstring for BasicChatbotNode
    """
    def __init__(self,model):
        self.llm = model 

    def process(self,state:State) -> dict : 
        """
        Docstring for process
        
        :param self: Description
        :param state: Description
        :type state: State
        :return: Description
        :rtype: dict
        """

        return {"messages":self.llm.invoke(state['messages'])}
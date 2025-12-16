from src.langgraphagenticai.state.state import State

class chatbot_tool_node: 
    """
    Docstring for chatbot_tool_node
    """
    def __init__(self,model) : 
        self.llm = model 


    def process (self,state:State) -> dict : 
        """
        Docstring for process
        
        :param self: Description
        :param state: Description
        :type state: State
        :return: Description
        :rtype: dict
        """

        user_input = state['messages'][-1] if state['messages'] else ""
        llm_response = self.llm.invoke([{"role":"user","content":user_input}])

        tools_response = f"Tool integration for {user_input}"
        return{"messages":[llm_response,tools_response]}
    


    def create_chatbot(self,tools) : 
        """
        Docstring for create_chatbot
        
        :param self: Description
        :param tools: Description
        """
        llm_with__tools = self.llm.bind_tools(tools)

        def chatbot_node(state:State) : 
            """
            Docstring for chatbot_node
            
            :param state: Description
            :type state: State
            """
            return {"messages":[llm_with__tools.invoke(state['messages'])]}    

        return chatbot_node


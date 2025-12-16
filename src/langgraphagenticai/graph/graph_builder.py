from langgraph.graph import StateGraph
from langgraph.graph import START , END
from src.langgraphagenticai.state.state import State
from src.langgraphagenticai.nodes.basic_chatbot_node import BasicChatbotNode
from src.langgraphagenticai.nodes.chatbot_with_tool_nodes import chatbot_tool_node
from src.langgraphagenticai.tools.search_tool import get_tools , create_tool_node
from langgraph.prebuilt import tools_condition,ToolNode

class GraphBuilder : 
    def __init__ (self,model):
        self.llm = model 
        self.graph_builder = StateGraph(State)


    def basic_chatbot_build_graph(self) : 
        self.basic_chatbot_node = BasicChatbotNode(self.llm)

        self.graph_builder.add_node("chatbot",self.basic_chatbot_node.process)

        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_edge("chatbot",END)

    def chatbot_with_tools_build_graph(self) : 
        """
        Docstring for chatbot_with_tools_build_graph
        
        :param self: Description
        """

        tools = get_tools()
        tool_node = create_tool_node(tools)

        llm = self.llm

        obj_chatbot_with_node = chatbot_tool_node(llm)
        chatbot_node = obj_chatbot_with_node.create_chatbot(tools=tools)
        
        self.graph_builder.add_node("chatbot",chatbot_node)
        self.graph_builder.add_node("tools",tool_node)

        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_conditional_edges("chatbot",tools_condition)
        self.graph_builder.add_edge("tools","chatbot")
        self.graph_builder.add_edge("chatbot",END)




    def setup_graph(self, usecase: str):
        usecase = usecase.strip().lower()

        builders = {
            "basic chatbot": self.basic_chatbot_build_graph,
            "basic chatbot with web" : self.chatbot_with_tools_build_graph
        }

        if usecase not in builders:
            raise ValueError(f"Unknown usecase: {usecase}")

        builders[usecase]()
        return self.graph_builder.compile()
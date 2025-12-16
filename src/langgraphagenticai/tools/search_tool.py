from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode


def get_tools():
    """
    Docstring for get_tools
    """

    tools = [TavilySearchResults(max_results=2)]
    return tools


def create_tool_node(tools) : 
    """
    Docstring for create_tool_node
    
    :param tools: Description
    """
    return ToolNode(tools=tools)
from pydantic import BaseModel , Field
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict , Annotated

class State (TypedDict) : 
    """
    Docstring for State
    """

    messages : Annotated[list,add_messages]
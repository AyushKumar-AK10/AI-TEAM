from langchain_core.messages import AIMessage
from langgraph.graph import MessagesState

from ..Output.output import devOutput


class State(MessagesState):
    userReq: str
    baResponse: AIMessage
    architectResponse: AIMessage
    devResponse: devOutput
    testResponse: AIMessage
    architectReview: AIMessage
    terminalRequester: str

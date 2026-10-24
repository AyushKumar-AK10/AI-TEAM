from langchain_core.messages import AIMessage,HumanMessage
from langgraph.graph import MessagesState

from ..Output.output import devOutput


class State(MessagesState):
    userReq: str
    baResponse: AIMessage
    architectResponse: AIMessage
    devResponse: devOutput
    testResponse: AIMessage
    testReview: AIMessage
    architectReview: AIMessage
    archReview: AIMessage
    terminalRequester: str
    githubApproval: HumanMessage

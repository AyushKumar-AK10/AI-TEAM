from langgraph.prebuilt.tool_node import ToolNode
from .terminal import execTerminal

tools = [execTerminal]
tool_node = ToolNode(tools=tools)
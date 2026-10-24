from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from .nodes import architectNode, baNode, developerNode, testerNode, architectReview,githubNode
from .state import State
from ..tools.toolNode import tool_node
from langgraph.prebuilt import tools_condition
from ..routes.route import tester_dev,architectReview_dev, terminalRoute, gitHubRouter

# Creating StateGraph
graph_builder = StateGraph(State)

# Adding Nodes to the Graph
graph_builder.add_node("baNode", baNode)
graph_builder.add_node("architectNode", architectNode)
graph_builder.add_node("devNode",developerNode)
graph_builder.add_node("testerNode", testerNode)
graph_builder.add_node('toolNode',tool_node)
graph_builder.add_node("architectReview",architectReview)
graph_builder.add_node("githubNode",githubNode)

# Adding Edges to the Graph
graph_builder.add_edge(START, "baNode")
graph_builder.add_edge("baNode", "architectNode")
graph_builder.add_edge("architectNode", "devNode")
graph_builder.add_edge("devNode", "testerNode")
graph_builder.add_conditional_edges(
    'testerNode',
    tester_dev,
    {
        "retry":"devNode",
        "tool_node":"toolNode",
        "review":"architectReview"
    }
)
graph_builder.add_conditional_edges(
    'architectReview',
    architectReview_dev,
    {
        "retry":"devNode",
        "END":'githubNode',
        "tool_node":'toolNode'
    }
)
graph_builder.add_conditional_edges(
    'toolNode',
    terminalRoute,
    {
        'tester':'testerNode',
        'architect':'architectReview',
        "github": 'githubNode'
    }
)

graph_builder.add_conditional_edges(
    'githubNode',
    gitHubRouter,
    {
        "END":END,
        "terminal":"toolNode"
    }
)

# Adding Checkpointing to the Graph
checkpointer = InMemorySaver()

# Compiling Graph
graph = graph_builder.compile(checkpointer=checkpointer)

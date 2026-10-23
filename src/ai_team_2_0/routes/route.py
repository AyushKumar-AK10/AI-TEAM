from ..graph.state import State

def tester_dev(state:State):
    if state.get('testResponse') and state.get('testResponse').content=='SUCCESS':
        return "review"
    elif state.get('testResponse'):
        return "retry"
    if state.get('messages')[-1].tool_calls:
        return "tool_node"

def architectReview_dev(state:State):
    if state.get('architectReview') and state.get('architectReview').content=='SUCCESS':
        return "END"
    elif state.get('architectReview'):
        return "retry"
    return "tool_node"

def terminalRoute(state:State):
    if state.get('terminalRequester')=="tester":
        return "tester"
    return "architect"
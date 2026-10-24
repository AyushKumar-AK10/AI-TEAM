from ..graph.state import State

def tester_dev(state:State):
    if state.get('messages')[-1].tool_calls:
        return "tool_node"
    elif state.get('testResponse') and state.get('testResponse').content=='SUCCESS':
        return "review"
    else:
        return "retry"
    

def architectReview_dev(state:State):
    if state.get('architectReview') and state.get('architectReview').content=='APPROVED':
        return "END"
    elif state.get('architectReview'):
        return "retry"
    return "tool_node"

def terminalRoute(state:State):
    if state.get('terminalRequester')=="tester":
        return "tester"
    return "architect"
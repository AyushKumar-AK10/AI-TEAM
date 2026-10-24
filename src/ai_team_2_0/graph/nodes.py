import json
from langchain_core.messages import AIMessage, HumanMessage,ToolMessage
from langgraph.graph.message import REMOVE_ALL_MESSAGES
from langgraph.types import interrupt
from ..config import architectPrompt, baPrompt, devPrompt, testerPrompt, architectReviewPrompt, githubPrompt
from ..models.gemini import devllm, llm, termllm
from ..tools.fileCreation import fc
from ..tools.terminal import execTerminal
from .state import State

# BA Node
async def baNode(state: State):
    '''BA Node Responsible for collecting the requirements from the user and generating the SRS document. '''
    prompt = [
        baPrompt.BaPrompt,
        HumanMessage(content=state["userReq"]),
    ]
    result = llm.invoke(prompt)
    result = json.loads(result.content[0]['text'])
    while result['status'] == "CLARIFICATION_REQUIRED":
        clarifications = interrupt(result['questions']) 
        result = llm.invoke(
            [
                *prompt,
                result['summary'],
                HumanMessage(content=f"User clarifications: {clarifications}"),
            ]
        )
        result = json.loads(result.content[0]['text'])
    return{
        "baResponse": AIMessage(content=result['srs']),
    }

# Architect Node
async def architectNode(state: State):
    '''Architect Node Responsible for generating the architecture document based on the SRS document. '''
    prompt = architectPrompt.ArchitectPrompt
    response = []
    async for chunk in llm.astream([prompt,state['baResponse'].content]):
        content = chunk.text
        print(content,end='',flush=True)
        response.append(content)
    return {
        "architectResponse": AIMessage("".join(response)),
    }

# Developer Node
async def developerNode(state:State):
    """Generate the project files."""
    prompt = devPrompt.DevPrompt
    history = []
    if state.get('devResponse'):
        history.append(f'Previous Developer Response{state.get('devResponse').model_dump_json()}')
    if state.get('testReview'):
        history.append(f'Tester Review: {state.get('testReview').content}')
    if state.get('archReview'):
        history.append(f'Architect Review: {state.get('archReview').content}')
    response = await devllm.ainvoke([prompt,state['architectResponse'].model_dump_json(),*history])   
    await fc.ainvoke({"devOutput": json.loads(response.model_dump_json())['output']})
    return{
        "devResponse": response
    }

# Creating the Tester node 
async def testerNode(state: State):
    """Run project checks through the terminal and report evidence-based results."""
    prompt = testerPrompt.TesterPrompt
    history = state.get('messages', [])
    if not history or not isinstance(history[-1], ToolMessage):
        history = []
    response = await termllm.ainvoke([prompt,HumanMessage(state['devResponse'].model_dump_json()),*history])
    if not response.tool_calls:
        result = json.loads(response.content[0]['text'])
        return{
            "testResponse": AIMessage(content=result['status']),
            "testReview": AIMessage(content=result['description']),
            "messages": [response]
        }
    return{
        "messages": [response],
        "terminalRequester":'tester'
    }

# Creating Architect Review Node
async def architectReview(state:State):
    '''Architect Review Node for reviewing the generated Project'''
    prompt = architectReviewPrompt.reviewPrompt
    history = state.get('messages', [])
    if not history or not isinstance(history[-1], ToolMessage):
        history = []
    response = await termllm.ainvoke([prompt,
    state['baResponse'],
    state['architectResponse'],
    HumanMessage(state['devResponse'].model_dump_json()),
    *history])
    if not response.tool_calls:
        result = json.loads(response.content[0]['text'])
        return{
            'architectReview': AIMessage(content=result['status']),
            'archReview': AIMessage(content=result['description']),
            'messages': [response]
        }
    else:
        return{
            'messages': [response],
            'terminalRequester':'architect'
        }

# Github Node
async def githubNode(state:State):
    prompt = githubPrompt.githubPrompt
    if not state.get('githubApproval'):
        approval = interrupt("Do you want to Publish to GitHub (Y/N)?")
        state['githubApproval']= HumanMessage(content=approval)
    messages = state.get('messages',[])
    history = []
    if messages and isinstance(messages[-1], ToolMessage):
        history = messages
    response = None
    if approval:
        response = await termllm.ainvoke([prompt,approval,*history])
        if not response.tool_calls:
            state['githubResponse']=response
        return{
            'terminalRequester': 'github',
            'messages': [response]
        }
    else:
        return{
            "githubResponse": AIMessage(content="The user didn't opt for Github Publish")
        }


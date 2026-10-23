from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from ..tools.terminal import execTerminal
from ..Output import output

load_dotenv()

# General LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite"
)
#  Developer LLM
devllm = llm.with_structured_output(output.devOutput)

#  Terminal LLM
tools = [execTerminal]
termllm = llm.bind_tools(tools)


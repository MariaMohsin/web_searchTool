from agents import Agent,AsyncOpenAI,OpenAIChatCompletionsModel,set_tracing_disabled,function_tool,Runner
from dotenv import load_dotenv
import os
from tavily import TavilyClient

load_dotenv()

gemini_api_key = os.environ.get("GEMINI_API_KEY")
tavily_api_key = os.environ.get("TAVILY_API_KEY")

set_tracing_disabled(True)

if not gemini_api_key or not tavily_api_key:
    raise ValueError("Please set the gemini or tavily api key in the .env file")
tavily_client = TavilyClient(api_key=tavily_api_key)

client=AsyncOpenAI(api_key=gemini_api_key,
                   base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

@function_tool
def web_search(query : str) -> str:
    """ Web search Provider"""
    print("[DEBUG] Web search function")
    response = tavily_client.search(query)
    return response 


@function_tool
def sum(a: int, b:int) -> int:
    """Returns the sum of two integers."""
    print("[DEBUG] Sum function")
    sum : int = a + b
    return sum

@function_tool
def subtraction(a: int, b:int) -> int:
    """Returns the subtraction of two integers."""
    print("[DEBUG] subtraction function")
    sub : int = a - b
    return sub


model=OpenAIChatCompletionsModel(openai_client=client,model="gemini-2.0-flash")

agent = Agent(
    name="General Assistant",
    instructions="You are a general assistant. Use the web_search tool when the user asks about real-world or factual information",
    model=model,
    tools=[sum, subtraction,web_search]
)

result = Runner.run_sync(agent,"hi,please tell me about Zia khan who is the CEO of Panaversity.")
print(result.final_output)

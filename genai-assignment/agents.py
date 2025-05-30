from system_prompts import rag_system_prompt, tool_agent_system_prompt, fallback_system_prompt, planning_agent_system_prompt, reviewer_system_prompt
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from config import client, chroma_user_memory
from autogen_core.tools import FunctionTool
from tools import calculate, get_weather
from output_parsers import RAGOutput, ToolOutput, ReviewOutput, FallbackOutput

# user_proxy_agent = UserProxyAgent(
#     name="user_proxy_agent",
#     human_input_mode="ALWAYS", 
#     code_execution_config=False,
# )

planning_agent = AssistantAgent(
    "PlanningAgent",
    description="An agent for planning tasks. This agent should be the first to engage when given a new task and will coordinate other agents (RAG, Tool, Fallback) to fulfill the request based on a defined workflow. It decides the sequence of agent execution.",
    model_client=client,
    system_message=planning_agent_system_prompt,
)

rag_agent = AssistantAgent(
    name="rag_agent",
    description="Answers user questions based SOLELY on retrieved content from a document vector store. It should be tried first for information retrieval tasks. It outputs its answer in a structured RAGOutput format, indicating its confidence.",
    model_client=client,
    memory=[chroma_user_memory],
    system_message=rag_system_prompt,
    output_content_type=RAGOutput
)

###### TOOLS - START ######
calculate_tool = FunctionTool(
    calculate, 
    description="Calculates the result of a simple arithmetic expression. For example, '2 + 2' or '10 * (5 - 2) / 3'.",
    strict=True
)

get_weather_tool = FunctionTool(
    get_weather,
    description="Provides a mock weather forecast for a given city (e.g., 'London', 'New York').",
    strict=True
)
###### TOOLS - END ######

tool_agent = AssistantAgent(
    name="tool_agent",
    description="Uses specific tools to answer queries when document retrieval (RAG) is insufficient or not applicable. Currently equipped with a 'calculator' for math expressions and a 'get_weather' tool for mock weather forecasts. Only use if the query directly implies a need for these tools and RAG agent was not confident.",
    model_client=client,
    system_message=tool_agent_system_prompt,
    tools=[calculate_tool, get_weather_tool],
    output_content_type=ToolOutput
)

llm_fallback_agent = AssistantAgent(
    name="llm_fallback_agent",
    description="A general-purpose AI assistant that provides answers based on broad knowledge. This agent is used as a last resort if both the RAG agent (document retrieval) and the Tool agent (specific tools) are unable to address the user's query satisfactorily.",
    model_client=client,
    system_message=fallback_system_prompt,
    output_content_type=FallbackOutput
)

reviewer_agent = AssistantAgent(
    name="reviewer_agent",
    description="A reviewer agent that reviews the answers provided by the RAG, Tool, and Fallback agents. It provides feedback on the quality of the answer and the confidence scores assigned by each agent.",
    model_client=client,
    system_message=reviewer_system_prompt,
    output_content_type=ReviewOutput
)


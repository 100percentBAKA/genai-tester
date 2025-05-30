from config import termination
import asyncio
from config import client, termination
from system_prompts import selector_prompt 
from agents import planning_agent, rag_agent, tool_agent, llm_fallback_agent
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.ui import Console


async def main():
    test_agent = rag_agent
    task = "Who is Johnathan Reynolds ?"

    await Console(test_agent.run_stream(task=task))


if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import logging
from config import termination
from config import client, termination
from system_prompts import selector_prompt 
from agents import planning_agent, rag_agent, tool_agent, llm_fallback_agent, reviewer_agent
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.ui import Console
from autogen_agentchat import EVENT_LOGGER_NAME, TRACE_LOGGER_NAME

logging.basicConfig(level=logging.WARNING)

# For trace logging.
trace_logger = logging.getLogger(TRACE_LOGGER_NAME)
trace_logger.addHandler(logging.StreamHandler())
trace_logger.setLevel(logging.DEBUG)

# For structured message logging, such as low-level messages between agents.
event_logger = logging.getLogger(EVENT_LOGGER_NAME)
event_logger.addHandler(logging.StreamHandler())
event_logger.setLevel(logging.DEBUG)


async def main():
    team = SelectorGroupChat(
        [planning_agent, rag_agent, tool_agent, llm_fallback_agent, reviewer_agent],
        model_client=client,
        termination_condition=termination,
        selector_prompt=selector_prompt,
        allow_repeated_speaker=True, 
    )

    task = "Who is Johnathan Reynolds ?"

    await Console(team.run_stream(task=task))


if __name__ == "__main__":
    asyncio.run(main())

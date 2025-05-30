import asyncio 
import logging

from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat import EVENT_LOGGER_NAME, TRACE_LOGGER_NAME
from autogen_agentchat.ui import Console

from agents import product_owner_agent, planner_agent, senior_developer_agent, junior_developer_agent, tester_agent
from config import termination, client
from prompts.system_prompts import selector_prompt

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
        [product_owner_agent, planner_agent, senior_developer_agent, junior_developer_agent, tester_agent],
        model_client=client,
        termination_condition=termination,
        selector_prompt=selector_prompt,
        allow_repeated_speaker=True, 
    )

    task = "Build a single page portfolio website for a financial advisor."

    await Console(team.run_stream(task=task))


if __name__ == "__main__":
    asyncio.run(main())

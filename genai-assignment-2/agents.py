from autogen_agentchat.agents import UserProxyAgent, AssistantAgent
from config import client
from prompts.system_prompts import (
    product_owner_system_prompt, 
    planner_system_prompt, 
    senior_developer_system_prompt,
    junior_developer_system_prompt,
    tester_system_prompt,
    deployer_system_prompt
)

####### AGENTS START #######
product_owner_agent = AssistantAgent(
    name="Product_Owner",
    description="Product Owner: Defines features, clarifies, and performs final acceptance of deployed product.",
    model_client=client,
    system_message=product_owner_system_prompt,
)

planner_agent = AssistantAgent(
    name="Planner",
    description="Planner: Creates overall plan & tech stack. Coordinates changes. Hands off to Senior Developer.",
    model_client=client,
    system_message=planner_system_prompt,
)

senior_developer_agent = AssistantAgent(
    name="Senior_Developer",
    description="Senior Developer: Reviews plan, creates two implementation phases for Junior Developer, oversees, hands to Deployer.",
    model_client=client,
    system_message=senior_developer_system_prompt,
)

junior_developer_agent = AssistantAgent(
    name="Junior_Developer",
    description="Junior Developer: Implements phases with code snippets, works with Tester.",
    model_client=client,
    system_message=junior_developer_system_prompt,
)

tester_agent = AssistantAgent(
    name="Tester",
    description="Tester: Tests phases from Junior Developer (reflecting on code snippets), provides feedback, approves phases.",
    model_client=client,
    system_message=tester_system_prompt,
)

deployer_agent = AssistantAgent(
    name="Deployer",
    description="Deployer: Simulates deployment of the tested feature with deployment scripts/code, hands off to Product Owner.",
    model_client=client,
    system_message=deployer_system_prompt,
)

# user_proxy_agent = UserProxyAgent(
#     name="user_proxy_agent",
#     human_input_mode="ALWAYS", 
#     code_execution_config=False,
# )

##### AGENTS END ######






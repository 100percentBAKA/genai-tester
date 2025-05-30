from dotenv import load_dotenv
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination

load_dotenv()

MAX_REVIEW_ITERATIONS = 2

client = OpenAIChatCompletionClient(model="gpt-4.1-mini-2025-04-14")

text_mention_termination = TextMentionTermination("TERMINATE")
max_messages_termination = MaxMessageTermination(max_messages=25)
termination = text_mention_termination | max_messages_termination
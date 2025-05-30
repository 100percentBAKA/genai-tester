from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.models.lite_llm import LiteLlm
from adk_tools.literature_search_tool import search_relevant_articles


# --- Agent Configuration ---
# Example: Using LiteLLM for OpenAI and Anthropic, and keeping Gemini for Validator
# Ensure you have OPENAI_API_KEY and ANTHROPIC_API_KEY in your .env file
SEARCH_AGENT_MODEL = LiteLlm("openai/gpt-3.5-turbo") 
SUMMARIZER_AGENT_MODEL = LiteLlm("anthropic/claude-3-haiku-20240307")
VALIDATOR_AGENT_MODEL = "gemini-1.5-pro-latest" # Placeholder - REPLACE THIS or use LiteLlm too

# --- 1. Define Sub-Agents for Each Pipeline Stage ---
search_agent = LlmAgent(
    name="SearchAgent",
    model=SEARCH_AGENT_MODEL, # Using LiteLlm model for SearchAgent
    instruction=(
        "You are a Research Assistant. Your goal is to retrieve relevant articles for a given query using the `search_relevant_articles` tool. "
        "The user will provide an initial query. Pass this query directly to the `search_relevant_articles` tool. "
        "Ensure you request a reasonable number of results (e.g., 3-5)."
        "The output of this step should be the direct result from the `search_relevant_articles` tool."
    ),
    description="Retrieves relevant articles from a vector database based on a query.",
    tools=[search_relevant_articles],
    output_key="retrieved_articles"
)

summarizer_agent = LlmAgent(
    name="SummarizerAgent",
    model=SUMMARIZER_AGENT_MODEL, # Using LiteLlm model for SummarizerAgent
    instruction=(
        "You are a Summarization Specialist. You will receive a list of retrieved articles under the key `retrieved_articles`. "
        "Your task is to synthesize the information from these articles into a single, coherent summary. "
        "The summary should be concise, capture the key points, and be easy to understand. "
        "Focus on extracting the most critical information relevant to the original research query (which you won't see directly, so summarize broadly based on the provided texts). "
        "If the `retrieved_articles` list contains a note about no documents being found or an error, your summary should reflect that, e.g., 'No relevant articles were found to summarize.' or 'An error occurred during search.'"
        "Output only the summary text."
        "Input documents will be in the format: {retrieved_articles}"
    ),
    description="Summarizes a list of documents into a concise overview.",
    output_key="summary_text"
)

validator_agent = LlmAgent(
    name="ValidatorAgent",
    model=VALIDATOR_AGENT_MODEL, # Keeping Gemini for Validator, or change as needed
    instruction=(
        "You are a Critical Reviewer and Validation Expert. You will receive a summary of literature under the key `summary_text`. "
        "Your task is to critically evaluate this summary.\n\n"
        "1. **Quality Check**: Assess clarity, coherence, and completeness of the `{summary_text}`. Does it make sense? Is it well-written?\n"
        "2. **Novelty/Insight (Conceptual)**: Based *only* on the `{summary_text}`, does the information presented seem insightful or merely superficial? (You don't have the original articles, only the summary). Guess if it adds value.\n"
        "3. **Potential Gaps/Questions**: Identify any obvious gaps or areas in the `{summary_text}` that might need further clarification if this were part of a real literature review. Formulate 1-2 key questions that a researcher might ask next based on this summary.\n"
        "4. **Decision & Rationale**: Provide a brief decision: 'ACCEPT', 'ACCEPT WITH MINOR REVISIONS', or 'NEEDS SIGNIFICANT REVISION'. Justify your decision concisely.\n\n"
        "Output your evaluation as a single text block. Start with your decision, then rationale, then any questions.\n"
        "Example Output:\n"
        "DECISION: ACCEPT WITH MINOR REVISIONS\n"
        "RATIONALE: The summary is well-structured and captures the main points effectively. However, it could be strengthened by elaborating slightly on the methodologies mentioned.\n"
        "QUESTIONS:\n"
        "- Can you provide more specific examples of the 'key methods' mentioned?\n"
        "- What were the limitations acknowledged in the original articles, if any, as per the summary?"
        "Input summary will be: {summary_text}"
    ),
    description="Validates a literature summary, suggests improvements, and makes a final judgment.",
    output_key="validation_output"
)

# --- 2. Create the SequentialAgent for the Literature Review Pipeline ---
literature_review_pipeline = SequentialAgent(
    name="LiteratureReviewPipeline",
    sub_agents=[search_agent, summarizer_agent, validator_agent],
    description="Executes a sequential pipeline of searching, summarizing, and validating literature.",
)

root_agent = literature_review_pipeline 
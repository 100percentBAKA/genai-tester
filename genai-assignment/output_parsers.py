from pydantic import BaseModel, Field
from typing import Optional, List
from config import MAX_REVIEW_ITERATIONS

class ReviewOutput(BaseModel):
    """Structured output for the Reviewer Agent with safeguards against infinite improvement loops."""
    is_sufficient: bool = Field(description="True if the provided answer is considered sufficient and addresses the query adequately, False otherwise.")
    critique: str = Field(description="Constructive critique of the answer, highlighting any issues or areas for improvement.")
    improvement_needed: bool = Field(description="Boolean flag indicating whether improvement is actually needed. Should be False if the answer is already good enough despite minor critiques.")
    improvement_priority: Optional[str] = Field(None, description="If improvement is needed, specify ONE key priority area: 'accuracy', 'completeness', 'clarity', or 'relevance'.")
    specific_correction: Optional[str] = Field(None, description="If there's a factual error or specific issue, provide the exact correction. Keep this VERY brief and targeted. Leave empty if no specific correction is needed.")
    iteration_count: int = Field(description=f"Counter for improvement iterations. When this reaches {MAX_REVIEW_ITERATIONS}, no further improvements should be requested regardless of quality.")

class RAGOutput(BaseModel):
    """Structured output for the RAG Agent with fields useful for review."""
    answer: str = Field(description="The generated answer to the user's query based on the retrieved context.")
    confidence_score: float = Field(description="A score from 0.0 to 1.0 indicating the RAG agent's confidence level in its answer based on the retrieved context.")
    reasoning: str = Field(description="Brief explanation of why the RAG agent assigned this confidence score to its answer.")

class ToolOutput(BaseModel):
    """Structured output for the Tool Agent with fields useful for review."""
    answer: str = Field(description="The generated answer to the user's query using available tools.")
    confidence_score: float = Field(description="A score from 0.0 to 1.0 indicating the Tool agent's confidence level in its answer based on tool execution.")
    reasoning: str = Field(description="Brief explanation of why the Tool agent assigned this confidence score to its answer.")

class FallbackOutput(BaseModel):
    """Structured output for the Fallback Agent with fields useful for review."""
    answer: str = Field(description="The generated answer to the user's query using the fallback agent.")
    confidence_score: float = Field(description="A score from 0.0 to 1.0 indicating the Fallback agent's confidence level in its answer.")
    reasoning: str = Field(description="Brief explanation of why the Fallback agent assigned this confidence score to its answer.")



from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.memory.chromadb import ChromaDBVectorMemory, PersistentChromaDBVectorMemoryConfig
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination

PDF_PATH = "Documents/random_person_bio.pdf"
CHROMA_COLLECTION_NAME = "document_embeddings_collection" 
CHROMA_PERSISTENCE_PATH = "./vector_store/chroma_db_store"  

MAX_REVIEW_ITERATIONS = 2

client = OpenAIChatCompletionClient(model="gpt-4.1-mini-2025-04-14")

chroma_user_memory = ChromaDBVectorMemory(
        config=PersistentChromaDBVectorMemoryConfig(
            collection_name=CHROMA_COLLECTION_NAME,
            persistence_path=CHROMA_PERSISTENCE_PATH,
            k=3,  
            score_threshold=0.4, 
        )
    )

text_mention_termination = TextMentionTermination("TERMINATE")
max_messages_termination = MaxMessageTermination(max_messages=25)
termination = text_mention_termination | max_messages_termination
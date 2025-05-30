import chromadb
import chromadb.utils.embedding_functions as embedding_functions

from dotenv import load_dotenv

load_dotenv()


openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                model_name="text-embedding-3-small"
            )

google_ef  = embedding_functions.GoogleGenerativeAiEmbeddingFunction()

client = chromadb.PersistentClient(path="C:/Users/Adarsh G S/Documents/Github-VII/test/genai-assignment-4/resources/databases")

chroma_collection = client.get_or_create_collection(name="rag_collection", embedding_function=google_ef)
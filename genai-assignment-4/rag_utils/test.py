from config import chroma_collection

result = chroma_collection.query(
    query_texts=["What is the name of the person in the document?"],
    n_results=2
)

print(result)

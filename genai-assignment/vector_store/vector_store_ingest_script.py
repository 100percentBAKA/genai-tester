import asyncio
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from vector_store_utils import extract_text_from_pdf, chunker, index_chunks
from config import PDF_PATH, chroma_user_memory

async def perform_indexing() -> None:
    print(f"Starting indexing process for PDF: {PDF_PATH}")

    document_pages_content = extract_text_from_pdf(pdf_path=PDF_PATH)
    all_chunks = chunker(
        document_pages_content=document_pages_content,
        chunk_size=1500,
        chunk_overlap=300
    )

    total_chunks_added = await index_chunks(
        all_chunks=all_chunks, 
        memory=chroma_user_memory
    )

    if total_chunks_added > 0:
        print(f"Successfully indexed {total_chunks_added} chunk(s) into the vector store.")
    else:
        print("No new chunks were added to the vector store during indexing.")
    
    print("Indexing process completed.")


if __name__ == "__main__":
    try:
        asyncio.run(perform_indexing())
    except Exception as e:
        print(f"An error occurred during the indexing process: {e}")
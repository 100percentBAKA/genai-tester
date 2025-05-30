import asyncio
import os

from .custom_utils import extract_text_from_pdf, chunker, index_chunks


PDF_FILE_PATH = os.path.join("resources", "rag_documents", "random_person_bio.pdf")

async def main():
    """
    Main function to orchestrate the PDF processing and indexing.
    """
    print(f"Starting processing for PDF: {PDF_FILE_PATH}")

    # 1. Extract text from the PDF
    print("Extracting text from PDF...")
    document_pages = extract_text_from_pdf(PDF_FILE_PATH)
    if not document_pages:
        print(f"No text could be extracted from {PDF_FILE_PATH}. Exiting.")
        return
    print(f"Successfully extracted {len(document_pages)} pages.")

    # 2. Chunk the extracted text
    print("Chunking extracted text...")
    chunk_texts, metadatas, ids = chunker(document_pages_content=document_pages)
    if not chunk_texts:
        print("No chunks were created. Exiting.")
        return
    print(f"Successfully created {len(chunk_texts)} chunks.")

    # 3. Index the chunks
    print("Indexing chunks...")
    await index_chunks(chunk_texts, metadatas, ids)
    print("Successfully indexed chunks.")
    print("Indexing process completed.")

if __name__ == "__main__":
    asyncio.run(main())

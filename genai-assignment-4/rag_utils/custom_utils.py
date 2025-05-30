import fitz
import os
from typing import List, Dict

from config import chroma_collection

def extract_text_from_pdf(pdf_path: str) -> List[Dict[str, any]]:
    document_pages_content = []

    try:
        doc = fitz.open(pdf_path)
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text_content = page.get_text("text")

            # print(text_content)
            
            document_pages_content.append({"page_number": page_num + 1, "text": text_content, "source": pdf_path})
        doc.close()

    except Exception as e:
        print(f"Error reading PDF file: {e}")
    
    return document_pages_content


def chunker(document_pages_content: List[Dict[str, any]], chunk_size: int = 1500, chunk_overlap: int = 300) -> tuple[List[str], List[Dict[str, any]], List[str]]:
    all_chunk_texts = []
    all_metadatas = []
    all_ids = []
    chunk_counter = 0

    for page_data in document_pages_content:
        text = page_data["text"]
        page_number = page_data["page_number"]
        source = page_data["source"]
        start = 0

        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunk_text = text[start:end].strip()
            chunk_id = f"{os.path.basename(source)}_p{page_number}_c{chunk_counter}"

            all_chunk_texts.append(chunk_text)
            all_metadatas.append({
                "source": source,
                "page_number": page_number
            })
            all_ids.append(chunk_id)
            
            chunk_counter += 1
            if end == len(text):
                break
            start += (chunk_size - chunk_overlap)
            if start >= len(text): 
                break
             
    return all_chunk_texts, all_metadatas, all_ids


async def index_chunks(chunk_texts: List[str], metadatas: List[Dict[str, any]], ids: List[str]):
    """
        Performs indexing of the chunks in the database.
    """
    try:
        chroma_collection.add(
            documents=chunk_texts,
            metadatas=metadatas,
            ids=ids
        )
    except Exception as e:
        print(f"Error indexing chunks: {e}")

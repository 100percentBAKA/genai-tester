import fitz
import os
from typing import List, Dict
from autogen_ext.memory.chromadb import ChromaDBVectorMemory
from autogen_core.memory import MemoryContent, MemoryMimeType

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


def chunker(document_pages_content: List[Dict[str, any]], chunk_size: int = 1500, chunk_overlap: int = 300) -> List[Dict[str, any]]:
    all_chunks = []
    chunk_counter = 0

    for page_data in document_pages_content:
        text = page_data["text"]
        page_number = page_data["page_number"]
        source = page_data["source"]
        start = 0

        while start < len(text):
             end = min(start + chunk_size, len(text))
             chunk_text = text[start:end]
             all_chunks.append({
                 "text": chunk_text.strip(),
                 "source": source,
                 "page_number": page_number,
                 "chunk_id": f"{os.path.basename(source)}_p{page_number}_c{chunk_counter}"
             })
             chunk_counter += 1
             if end == len(text):
                 break
             start += (chunk_size - chunk_overlap)
             if start >= len(text): 
                 break
             
    return all_chunks


async def index_chunks(all_chunks: List[Dict[str, any]], memory: ChromaDBVectorMemory) -> int:
    """
        Performs indexing of the chunks

        Returns: total number of chunks indexed
    """
    total_chunks_added = 0

    for chunk_data in all_chunks:
        try:
            await memory.add(
                MemoryContent(
                    content=chunk_data["text"],
                    mime_type=MemoryMimeType.TEXT,
                    metadata={
                        "source": chunk_data["source"],
                        "page_number": chunk_data.get("page_number", -1),
                        "chunk_id": chunk_data.get("chunk_id", "unknown")
                    }
                )
            )
            total_chunks_added += 1

        except Exception as e:
            print(f"Error adding chunk {chunk_data.get('chunk_id', 'unknown')} to memory: {e}")
    
    print(f"Successfully added {total_chunks_added} chunks to store.")
    return total_chunks_added


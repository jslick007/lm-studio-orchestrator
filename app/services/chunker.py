import tiktoken
from typing import List, Dict


def chunk_text(
    text: str, model: str = "gpt-3.5-turbo", chunk_size: int = 1024, overlap: int = 200
) -> List[Dict]:
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(text)

    chunks = []
    start = 0
    chunk_id = 0

    while start < len(tokens):
        end = start + chunk_size
        chunk_tokens = tokens[start:end]

        chunks.append(
            {
                "chunk_id": chunk_id,
                "text": encoding.decode(chunk_tokens),
                "start_token": start,
                "end_token": min(end, len(tokens)),
            }
        )

        chunk_id += 1
        # Move start forward by chunk_size minus overlap
        start += chunk_size - overlap

        # If we've reached the end of the tokens, break
        if end >= len(tokens):
            break

    return chunks

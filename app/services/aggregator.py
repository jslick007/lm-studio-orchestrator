from typing import List, Dict


def aggregate_responses(results: List[Dict]) -> str:
    # Sort results by chunk_id to ensure correct order
    sorted_results = sorted(results, key=lambda x: x["chunk_id"])

    aggregated_text = ""
    for res in sorted_results:
        # Extract the content from the OpenAI-style response
        try:
            content = res["response"]["choices"][0]["message"]["content"]
            aggregated_text += content + "\n"
        except (KeyError, IndexError):
            aggregated_text += f"[Error in chunk {res['chunk_id']}]: {res.get('response', 'Unknown error')}\n"

    return aggregated_text.strip()

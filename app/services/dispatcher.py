import httpx
import asyncio
from typing import List, Dict
from app.services import registry


async def dispatch_chunks(chunks: List[Dict]) -> List[Dict]:
    nodes = registry.get_nodes()
    if not nodes:
        raise Exception("No nodes registered in the registry")

    # Weighted distribution

    # Create a pool of nodes based on their weights

    node_pool = []
    for node in nodes:
        node_pool.extend([node] * node["weight"])

    tasks = []
    async with httpx.AsyncClient(timeout=None) as client:
        for i, chunk in enumerate(chunks):
            # Pick node from pool using round-robin on the pool
            node = node_pool[i % len(node_pool)]
            url = f"{node['url']}/chat/completions"

            # Prepare payload
            payload = {
                "messages": [{"role": "user", "content": chunk["text"]}],
                "model": "local-model",  # Default model name for LM Studio
            }

            tasks.append(send_chunk(client, url, payload, chunk["chunk_id"]))

        print(f"Firing {len(tasks)} concurrent requests across {len(nodes)} nodes...")
        results = await asyncio.gather(*tasks)

    return results


async def send_chunk(client, url, payload, chunk_id, max_retries=2):
    for attempt in range(max_retries + 1):
        try:
            print(f"Sending chunk {chunk_id} to {url} (Attempt {attempt + 1})...")
            response = await client.post(url, json=payload, timeout=30.0)
            if response.status_code == 200:
                return {
                    "chunk_id": chunk_id,
                    "response": response.json(),
                    "status": response.status_code,
                }
            else:
                print(f"Node {url} returned error {response.status_code}")
        except (httpx.RequestError, httpx.TimeoutException) as e:
            print(f"Request to {url} failed: {e}")

        if attempt < max_retries:
            # Try another node for retry
            nodes = registry.get_nodes()
            if nodes:
                # Pick a random different node if possible
                import random

                node = random.choice(nodes)
                url = f"{node['url']}/chat/completions"
            else:
                break

    return {
        "chunk_id": chunk_id,
        "response": {"error": "All retry attempts failed"},
        "status": 500,
    }

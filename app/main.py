import os
from fastapi import FastAPI, Request, HTTPException
from dotenv import load_dotenv
from app.services import registry, chunker, dispatcher, aggregator

load_dotenv()

app = FastAPI(title="LM Studio Map-Reduce Orchestrator")

LM_STUDIO_URL = os.getenv("LM_STUDIO_URL", "http://localhost:1234/v1")


@app.get("/nodes")
async def list_nodes():
    return registry.get_nodes()


@app.post("/nodes")
async def register_node(node: dict):
    if "url" not in node:
        raise HTTPException(status_code=400, detail="URL is required")
    url = node["url"]
    weight = node.get("weight", 1)
    return registry.add_node(url, weight)


@app.delete("/nodes/{url}")
async def unregister_node(url: str):
    if registry.remove_node(url):
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Node not found")


@app.post("/v1/chat/completions")
async def proxy_chat_completions(request: Request):
    body = await request.json()

    # Extract the user message to chunk
    messages = body.get("messages", [])
    if not messages:
        raise HTTPException(status_code=400, detail="No messages provided")

    user_text = messages[-1]["content"]

    # 1. Chunking
    chunks = chunker.chunk_text(user_text)

    # 2. Dispatching
    try:
        results = await dispatcher.dispatch_chunks(chunks)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # 3. Aggregation
    final_text = aggregator.aggregate_responses(results)

    # Return as OpenAI compatible response
    return {
        "id": "chatcmpl-orchestrator",
        "object": "chat.completion",
        "created": 0,
        "model": body.get("model", "local-model"),
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": final_text},
                "finish_reason": "stop",
            }
        ],
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

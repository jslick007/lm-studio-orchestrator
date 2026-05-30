# Handoff Prompts

### Task 1: Base Proxy Setup
**Context:** We are building a Map-Reduce Orchestrator for LM Studio. The first step is a simple proxy.
**Deliverable:** A FastAPI application with one endpoint `/v1/chat/completions` that takes an OpenAI-compatible JSON body and forwards it using `httpx` to a hardcoded LM Studio URL.
**Acceptance Check:** Successfully receive a response from LM Studio via the proxy.
**Constraints:** Use `FastAPI` and `httpx`.

### Task 2: Endpoint Registry
**Context:** We need to manage multiple LM Studio nodes.
**Deliverable:** Add a `/nodes` endpoint to the FastAPI app. Implement a simple in-memory list (or JSON file) that stores node objects containing `url`, `weight`, and `status`. Include GET (list) and POST (add) methods.
**Acceptance Check:** Be able to add three different local IP addresses to the registry via curl.
**Constraints:** Ensure weights are integers.

### Task 3: Registration Script
**Context:** Instead of manual API calls, we want a script for worker nodes to register themselves.
**Deliverable:** Create a `register_node.py` or shell script. It should detect the local IP, allow the user to specify a weight, and send a POST request to the Orchestrator's `/nodes` endpoint.
**Acceptance Check:** Running the script on a worker node automatically adds it to the orchestrator's node list.
**Constraints:** The script should be a single file with minimal dependencies (e.g., using `requests` or `curl`).

### Task 4: Deterministic Chunker
**Context:** We need to split long prompts to distribute them across nodes.
**Deliverable:** Create a `chunker.py` utility. It should take a string, a target number of chunks, and an `overlap_tokens` value. Use `tiktoken` to ensure splits happen on token boundaries.
**Acceptance Check:** A prompt of 1000 tokens split into 2 chunks with 100-token overlap should result in two chunks of roughly 550 tokens each.
**Constraints:** Use `cl100k_base` encoding.

### Task 4: Async Dispatcher
**Context:** We have chunks and nodes; now we need to execute in parallel.
**Deliverable:** Modify the `/v1/chat/completions` logic. Instead of one request, it should create a list of tasks (one per chunk) and use `asyncio.gather()` to fire them to different registered nodes simultaneously.
**Acceptance Check:** The logs should show requests hitting multiple different IPs at the same time.
**Constraints:** Use `httpx.AsyncClient`.

### Task 5: Sequence Aggregator
**Context:** Parallel responses arrive out of order.
**Deliverable:** Implement an aggregation layer that assigns a `chunk_id` to every request. Collect all responses into a dictionary, sort by `chunk_id`, and concatenate the `content` fields into a single string.
**Acceptance Check:** Ensure the final response doesn't have chunks swapped (e.g., Chunk 2 before Chunk 1).
**Constraints:** Handle cases where a chunk might return an empty string.

### Task 6: Weight-Based Load Balancer
**Context:** Nodes have different CPU speeds.
**Deliverable:** Update the Dispatcher. Instead of Round Robin, distribute chunks based on the `weight` in the registry. (e.g., if Node A weight=2 and Node B weight=1, Node A gets 66% of the chunks).
**Acceptance Check:** For 6 chunks and weights [2, 1], Node A should receive 4 requests and Node B should receive 2.
**Constraints:** Handle the remainder if chunks aren't perfectly divisible by weights.

### Task 7: Timeout & Failover
**Context:** CPU nodes can hang or crash.
**Deliverable:** Wrap the `httpx` calls in a timeout (e.g., 30s). If a request fails or times out, the aggregator should insert a marker like `[Chunk X failed]` into the final response rather than crashing the whole request.
**Acceptance Check:** Shut down one worker node; the final response should still return with the remaining chunks.
**Constraints:** Do not let one node stall the total response time beyond the timeout limit.

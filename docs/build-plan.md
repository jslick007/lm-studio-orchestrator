# Build Plan: Map-Reduce Orchestrator

| Turn | Task | Deliverable | Acceptance Check | Dependencies |
| :--- | :--- | :--- | :--- | :--- |
| 1 | **Base Proxy Setup** | FastAPI server that forwards a request to a single LM Studio endpoint. | Request to `/v1/chat/completions` returns a valid response from one node. | None |
| 2 | **Endpoint Registry** | A JSON-based registry to store multiple node URLs and weights. | Ability to add/remove endpoints via a simple `/nodes` API. | 1 |
| 3 | **Registration Script** | A lightweight script for worker nodes to "push" their registration. | Running the script on a node successfully adds it to the orchestrator's registry. | 2 |
| 4 | **Deterministic Chunker** | Logic to split a string into $N$ token-sized chunks with overlap. | A 2000-token prompt split into 3 chunks with 200-token overlaps. | 3 |
| 5 | **Async Dispatcher** | Logic to send $N$ chunks to $M$ nodes concurrently. | Log output showing multiple concurrent HTTP requests being fired. | 4 |
| 6 | **Sequence Aggregator** | Logic to collect responses and concatenate them by `chunk_id`. | Input "A+B+C" results in a response that is "Response A" + "Response B" + "Response C". | 5 |
| 7 | **Weight-Based Load Balancer** | Integration of endpoint weights into the chunk distribution logic. | Faster nodes (higher weight) are assigned more chunks than slower nodes. | 6 |
| 8 | **Timeout & Failover** | Implementation of request timeouts and "dead-node" skipping. | If one node is shut down, the request still completes (with a gap or retry). | 7 |

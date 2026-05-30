# User Stories: Map-Reduce Orchestrator

| Priority | Story | Acceptance Criteria | Version |
| :--- | :--- | :--- | :--- |
| 1 | **As a user**, I want to send a long prompt to the router so that it can be processed by multiple machines. | [ ] Router accepts OpenAI-compatible `/v1/chat/completions` request.<br>[ ] Input is successfully split into $N$ chunks based on available nodes. | v1 |
| 2 | **As a user**, I want the router to send chunks to different machines in parallel so that I don't have to wait for sequential processing. | [ ] HTTP requests to LM Studio endpoints are fired asynchronously.<br>[ ] All endpoints are utilized simultaneously. | v1 |
| 3 | **As a user**, I want the responses to be returned in the correct order so that the final text is coherent. | [ ] Responses are indexed by chunk ID.<br>[ ] Concatenation occurs in the original sequence of chunks. | v1 |
| 4 | **As a user**, I want to register machines with different "weights" so that my fast PC does more work than my old laptop. | [ ] Registry allows assigning a weight/capacity to each endpoint.<br>[ ] Chunks are distributed proportionally to weight. | v1 |
| 5 | **As a user**, I want a simple script I can run on my worker nodes to register them with the orchestrator automatically. | [ ] A registration script (curl/python) exists that sends the node's IP and weight to the orchestrator. | v1 |
| 6 | **As a user**, I want the system to skip a crashed machine so that one offline node doesn't hang my entire request. | [ ] Router implements a timeout per chunk.<br>[ ] Failed chunks are retried on a healthy node or reported as a gap in the final response. | v1 |
| 7 | **As a user**, I want the chunks to have overlapping context so that the AI doesn't lose the thread between splits. | [ ] Configurable "overlap" window (e.g., 200 tokens) is added to the start of each subsequent chunk. | v1 |
| 8 | **As a user**, I want to see the total TPS across the cluster so I can measure the speedup. | [ ] Response metadata includes the aggregate tokens per second. | v2 |

# Architecture: Map-Reduce Orchestrator

## High-Level Component Diagram
```text
[ Client ] 
    | (OpenAI API Request)
    v
[ Orchestrator ]
    |--> [ Chunker ] (Splits text + adds overlap)
    |--> [ Dispatcher ] (Weights chunks -> Endpoints)
    |--> [ Parallel Executor ] (Async HTTP Calls)
    |--> [ Aggregator ] (Re-orders + Concatenates)
    v
[ LM Studio Node A ] [ LM Studio Node B ] [ LM Studio Node C ]
    (CPU-Only)           (CPU-Only)           (CPU-Only)
        ^                     ^                     ^
        |                     |                     |
        +------- [ Registration Script ] -----------+
```

## Data Model
### Endpoint Registry
- `id`: UUID
- `url`: String (e.g., `http://192.168.1.15:1234/v1`)
- `weight`: Integer (Relative processing power, e.g., 1-10)
- `status`: Enum (Healthy, Unhealthy, Busy)
- `last_seen`: Timestamp

### Request State
- `request_id`: UUID
- `chunks`: List of `Chunk` objects
- `completion_status`: Percentage complete

### Chunk Object
- `chunk_id`: Integer (Sequence order)
- `content`: String (The prompt segment)
- `assigned_node`: Endpoint ID
- `result`: String (The generated response)

## Technical Choices
- **Language:** Python (FastAPI) — Best-in-class async support for handling multiple HTTP requests and excellent string/token manipulation libraries.
- **Async Library:** `httpx` — Required for non-blocking parallel requests to the LM Studio endpoints.
- **Tokenization:** `tiktoken` — To ensure deterministic splitting based on model token limits rather than character counts.

## Performance Goals
For complex, long-context queries distributed across $N$ CPU-only nodes:
- **Time to First Token (TTFT):** Target $2\times$ to $4\times$ reduction compared to a single node, by parallelizing the prefill phase.
- **Tokens Per Second (TPS):** Target near-linear scaling ($\approx N \times$ single-node TPS) by parallelizing the generation phase.

## Key Data Flow: The Map-Reduce Cycle
1. **Chunking:** The Orchestrator receives a prompt. It uses `tiktoken` to divide the prompt into $N$ segments. To prevent "edge loss," it implements a sliding window where each chunk $i$ starts with the last $X$ tokens of chunk $i-1$.
2. **Dispatching:** The Dispatcher checks the Registry. It assigns chunks to nodes based on `weight`. If Node A has weight 2 and Node B has weight 1, Node A receives two chunks for every one Node B receives.
3. **Execution:** `httpx.AsyncClient` fires requests to all assigned endpoints concurrently.
4. **Aggregation:** As responses arrive, they are stored in a map keyed by `chunk_id`. Once all requests resolve (or timeout), the Aggregator joins the strings in order.

## Risks & Unknowns
- **The Coherence Gap:** Because the model doesn't see the output of Chunk 1 when generating Chunk 2, the transition between concatenated blocks may be repetitive or disjointed. 
- **Network Jitter:** On a local CPU cluster, one slow WiFi connection could bottleneck the entire response (The "Straggler Problem").
- **Memory Limits:** Splitting a prompt too aggressively might lead to chunks that are too small to provide meaningful context.

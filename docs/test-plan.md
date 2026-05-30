# Test Plan: Map-Reduce Orchestrator

## Unit Test Targets
- **Chunker Logic:**
    - Verify that total tokens in chunks $\approx$ (Original Tokens + (Chunks-1 * Overlap)).
    - Verify that boundaries are on token edges, not mid-word.
- **Aggregation Logic:**
    - Verify that responses `[Chunk 2, Chunk 0, Chunk 1]` are concatenated as `0 -> 1 -> 2`.
- **Weighted Distribution:**
    - Verify that a node with weight 10 receives exactly 10x more chunks than a node with weight 1 given a large enough sample.

## Integration Test Scenarios
1. **The Happy Path:** 3 nodes registered $\rightarrow$ 1 long prompt $\rightarrow$ 3 parallel requests $\rightarrow$ 1 coherent concatenated response.
2. **The Straggler Test:** 2 nodes registered (one fast, one extremely slow). Verify that the total time is limited by the slow node's timeout, not an infinite hang.
3. **The Dead Node Test:** 3 nodes registered, one is powered off. Verify the system completes the request with a "Chunk Failed" marker.

## Manual QA Checklist
- [ ] **Coherence Check:** Paste the concatenated response into a text editor. Check the transition points between chunks for extreme repetition or abrupt cuts.
- [ ] **Latency Measurement:** Time a 5,000-token prompt on one machine vs. the Orchestrator with three machines.
- [ ] **API Compatibility:** Ensure a standard OpenAI client (like the Python `openai` library) can use the Orchestrator as the `base_url`.

## Test Data Strategy
- **Dataset:** Use long-form Wikipedia articles (5k+ tokens) to test chunking boundaries.
- **Environment:** Use three separate VMs or physical machines with different RAM/CPU profiles to simulate a heterogeneous cluster.

## Definition of "Done" (v1 Ship)
- [ ] All Unit Tests pass.
- [ ] Happy Path integration test completes successfully.
- [ ] **Performance Benchmark:** 
    - TTFT is at least $2\times$ faster than single-node for long prompts.
    - Aggregate TPS is $\approx N \times$ single-node TPS.
- [ ] The API responds to standard OpenAI-formatted requests.

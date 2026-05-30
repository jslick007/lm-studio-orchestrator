# Product Brief: LM Studio Map-Reduce Orchestrator

## Problem
LLM inference on CPU-only hardware is characterized by high latency and low tokens-per-second (TPS), making the processing of long-context prompts prohibitively slow for a single machine. While a user may have multiple CPU-capable machines, there is currently no native way to distribute a single large request across these machines to accelerate the time to a final response.

## Solution
The Map-Reduce Orchestrator is a routing layer that sits between the user and multiple LM Studio instances. It implements a deterministic "divide and conquer" strategy: it splits a long input prompt into overlapping chunks, distributes these chunks across a cluster of CPU-only endpoints in parallel, and concatenates the resulting partial responses into a single unified output.

## Target User
A power user or developer with a heterogeneous home/office lab of CPU-only machines running LM Studio, seeking to reduce the wall-clock time required to process large documents or long prompts.

## Core Value Proposition
Transform a slow, single-machine CPU experience into a high-throughput cluster experience by parallelizing the inference of long-context inputs.

## Estimated Performance Gains
For complex, long-context queries distributed across $N$ CPU-only nodes:
- **Time to First Token (TTFT):** Estimated $2\times$ to $4\times$ faster, as prefill is distributed across the cluster.
- **Tokens Per Second (TPS):** Near-linear increase ($\approx N \times$ single-node TPS), as generation occurs in parallel across multiple machines.

## Out of Scope for v1
- **Intelligent Decomposition:** No LLM-based planning or sub-task splitting.
- **Consensus/Voting:** No "Best-of-N" sampling or response merging via a second LLM pass.
- **GPU Orchestration:** Specifically optimized for the constraints of CPU-only nodes.
- **Dynamic Scaling:** No auto-scaling of nodes; nodes are registered via a lightweight registration script (Push model).

## Success Metric
**Wall-Clock Reduction:** The time from the initial request to the final concatenated response must be at least 30% faster than the same request processed by the fastest single node in the cluster (accounting for network overhead).

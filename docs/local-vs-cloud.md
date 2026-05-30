# Local vs. Cloud Distribution

Since this project is designed for a **local CPU-only cluster**, the deployment strategy is entirely on-premise.

| Task | Location | Reason |
| :--- | :--- | :--- |
| **Orchestrator API** | Local | Must have low-latency access to the local LAN to avoid adding to TTFT. |
| **Endpoint Registry** | Local | Stores local IP addresses of the CPU machines. |
| **Inference (LM Studio)** | Local | The core compute happens on the CPU-only machines. |
| **Tokenization** | Local | Happens within the Orchestrator before dispatching. |

## Local Environment Requirements
- **Network:** All machines must be on the same subnet.
- **Firewall:** Port `1234` (default LM Studio) must be open on all worker nodes.
- **Credentials:** No external cloud credentials required; uses local HTTP calls.

## Data Flow
`User Device` $\xrightarrow{HTTP}$ `Orchestrator Machine` $\xrightarrow{Parallel HTTP}$ `Worker Nodes` $\xrightarrow{Response}$ `Orchestrator Machine` $\xrightarrow{HTTP}$ `User Device`.

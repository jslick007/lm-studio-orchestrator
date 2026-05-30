import httpx
import argparse
import socket


def register_node(orchestrator_url, node_url=None, weight=1):
    if not node_url:
        # Try to guess the node's own URL
        hostname = socket.gethostname()
        # Assuming LM Studio is on 1234
        node_url = f"http://{hostname}:1234/v1"

    print(f"Registering node {node_url} with weight {weight} to {orchestrator_url}...")

    try:
        response = httpx.post(
            f"{orchestrator_url}/nodes", json={"url": node_url, "weight": weight}
        )
        if response.status_code == 200:
            print("Successfully registered!")
        else:
            print(f"Failed to register: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error during registration: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Register this node with the Orchestrator"
    )
    parser.add_argument(
        "--orchestrator",
        required=True,
        help="The URL of the orchestrator (e.g., http://orchestrator:8000)",
    )
    parser.add_argument(
        "--url", help="The URL of this LM Studio instance (defaults to auto-detected)"
    )
    parser.add_argument(
        "--weight", type=int, default=1, help="Weight of this node (default: 1)"
    )

    args = parser.parse_args()
    register_node(args.orchestrator, args.url, args.weight)

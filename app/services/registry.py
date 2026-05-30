import json
import os
from typing import List, Dict

REGISTRY_FILE = "registry.json"


def load_registry() -> List[Dict]:
    if not os.path.exists(REGISTRY_FILE):
        return []
    with open(REGISTRY_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_registry(registry: List[Dict]):
    with open(REGISTRY_FILE, "w") as f:
        json.dump(registry, f, indent=4)


def add_node(url: str, weight: int = 1):
    registry = load_registry()
    # Avoid duplicates
    registry = [node for node in registry if node["url"] != url]
    registry.append({"url": url, "weight": weight})
    save_registry(registry)
    return {"url": url, "weight": weight}


def remove_node(url: str):
    registry = load_registry()
    new_registry = [node for node in registry if node["url"] != url]
    if len(new_registry) == len(registry):
        return False
    save_registry(new_registry)
    return True


def get_nodes():
    return load_registry()

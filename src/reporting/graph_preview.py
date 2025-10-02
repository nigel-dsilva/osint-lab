import orjson as json
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime, timezone
from src.utils.env import load

def preview_graph():
    cfg = load()
    corr_dir = Path(cfg["project"]["correlation_dir"])

    # Default to today's graph file
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    graph_file = corr_dir / f"{stamp}.graphml"

    if not graph_file.exists():
        raise SystemExit(f"No graph file found: {graph_file}")

    # Load graph
    G = nx.read_graphml(graph_file)

    # Simple layout
    pos = nx.spring_layout(G, seed=42)

    plt.figure(figsize=(8,6))
    nx.draw_networkx_nodes(G, pos, node_size=500, node_color="skyblue")
    nx.draw_networkx_edges(G, pos, edge_color="gray")
    nx.draw_networkx_labels(G, pos, font_size=8)

    plt.title(f"Graph Preview ({stamp})")
    plt.axis("off")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    preview_graph()

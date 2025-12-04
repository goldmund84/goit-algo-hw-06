from __future__ import annotations

import json
from pathlib import Path

import networkx as nx

try:
    import matplotlib.pyplot as plt
except ImportError:  # pragma: no cover - optional dependency
    plt = None

from transport_network import analyze_graph, create_graph

FIGURE_PATH = Path(__file__).with_name("task-1-network.png")


def visualize_graph(graph: nx.Graph, output_path: Path = FIGURE_PATH) -> Path:
    if plt is None:
        raise RuntimeError("matplotlib is required to visualize the graph.")

    pos = nx.get_node_attributes(graph, "pos")
    edge_labels = nx.get_edge_attributes(graph, "distance")

    plt.figure(figsize=(10, 6))
    nx.draw_networkx(
        graph,
        pos=pos,
        with_labels=True,
        node_size=1200,
        node_color="#0077b6",
        font_size=10,
        font_color="white",
        edge_color="#8ecae6",
        width=2,
    )
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=8)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()
    return output_path


def main() -> None:
    graph = create_graph()
    summary = analyze_graph(graph)
    print("City transport network summary:")
    print(json.dumps(summary, indent=2))
    try:
        output = visualize_graph(graph)
    except RuntimeError as exc:
        print(f"Visualization skipped: {exc}")
    else:
        print(f"Graph visualization saved to: {output}")


if __name__ == "__main__":
    main()

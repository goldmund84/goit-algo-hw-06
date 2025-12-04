from __future__ import annotations

import json
from pathlib import Path

import networkx as nx

try:
    import matplotlib.pyplot as plt
except ImportError:  # pragma: no cover - optional dependency
    plt = None


CITIES = {
    "Kyiv": (30.5234, 50.4501),
    "Zhytomyr": (28.6767, 50.2547),
    "Vinnytsia": (28.4682, 49.2331),
    "Lviv": (24.0316, 49.8420),
    "Lutsk": (25.3244, 50.7472),
    "Lublin": (22.5684, 51.2465),
    "Warsaw": (21.0122, 52.2297),
    "Krakow": (19.9445, 50.0647),
}


ROUTES = [
    ("Kyiv", "Zhytomyr", 140),
    ("Zhytomyr", "Vinnytsia", 120),
    ("Vinnytsia", "Lviv", 360),
    ("Lviv", "Lutsk", 150),
    ("Lutsk", "Kyiv", 430),
    ("Lviv", "Lublin", 225),
    ("Lublin", "Warsaw", 170),
    ("Lviv", "Krakow", 330),
    ("Krakow", "Warsaw", 295),
    ("Lutsk", "Lublin", 180),
]

FIGURE_PATH = Path(__file__).with_name("task-1-network.png")


def create_graph() -> nx.Graph:
    graph = nx.Graph()
    for city, coords in CITIES.items():
        graph.add_node(city, pos=coords)
    for city_a, city_b, distance in ROUTES:
        graph.add_edge(city_a, city_b, distance=distance)
    return graph


def analyze_graph(graph: nx.Graph) -> dict[str, object]:
    num_nodes = graph.number_of_nodes()
    num_edges = graph.number_of_edges()
    degrees = dict(graph.degree())
    avg_degree = sum(degrees.values()) / num_nodes
    max_degree_city = max(degrees, key=degrees.get)
    min_degree_city = min(degrees, key=degrees.get)
    return {
        "nodes": num_nodes,
        "edges": num_edges,
        "average_degree": round(avg_degree, 2),
        "max_degree_city": max_degree_city,
        "max_degree": degrees[max_degree_city],
        "min_degree_city": min_degree_city,
        "min_degree": degrees[min_degree_city],
        "degrees": degrees,
    }


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

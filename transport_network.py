from __future__ import annotations

import networkx as nx

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


__all__ = ["CITIES", "ROUTES", "create_graph", "analyze_graph"]

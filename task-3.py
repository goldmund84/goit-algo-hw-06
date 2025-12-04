from __future__ import annotations

import heapq
from typing import Dict, List, Optional, Tuple

import networkx as nx

from transport_network import create_graph


def dijkstra(graph: nx.Graph, start: str) -> Tuple[Dict[str, float], Dict[str, Optional[str]]]:
    distances: Dict[str, float] = {node: float("inf") for node in graph.nodes}
    previous: Dict[str, Optional[str]] = {node: None for node in graph.nodes}
    distances[start] = 0.0

    priority_queue: List[Tuple[float, str]] = [(0.0, start)]

    while priority_queue:
        current_distance, node = heapq.heappop(priority_queue)
        if current_distance > distances[node]:
            continue

        for neighbor, attrs in graph[node].items():
            weight = float(attrs.get("distance", 1.0))
            new_distance = current_distance + weight
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = node
                heapq.heappush(priority_queue, (new_distance, neighbor))

    return distances, previous


def reconstruct_path(previous: Dict[str, Optional[str]], start: str, goal: str) -> Optional[List[str]]:
    if previous[goal] is None and start != goal:
        return None

    path: List[str] = [goal]
    while path[-1] != start:
        parent = previous[path[-1]]
        if parent is None:
            return None
        path.append(parent)
    path.reverse()
    return path


def all_pairs_shortest_paths(graph: nx.Graph) -> Dict[str, Dict[str, Tuple[float, Optional[List[str]]]]]:
    results: Dict[str, Dict[str, Tuple[float, Optional[List[str]]]]] = {}
    for start in graph.nodes:
        distances, previous = dijkstra(graph, start)
        per_start: Dict[str, Tuple[float, Optional[List[str]]]] = {}
        for goal in graph.nodes:
            path = reconstruct_path(previous, start, goal)
            per_start[goal] = (distances[goal], path)
        results[start] = per_start
    return results


def print_summary(summary: Dict[str, Dict[str, Tuple[float, Optional[List[str]]]]]) -> None:
    for start, targets in summary.items():
        print(f"\nНайкоротші шляхи з {start}:")
        for goal, (distance, path) in targets.items():
            if path is None:
                print(f"  -> до {goal}: недосяжно")
            else:
                path_str = ' -> '.join(path)
                print(f"  -> до {goal}: {distance:.0f} км ({path_str})")


def main() -> None:
    graph = create_graph()
    summary = all_pairs_shortest_paths(graph)
    print_summary(summary)


if __name__ == "__main__":
    main()

from __future__ import annotations

from collections import deque
from typing import Iterable, List, Optional

import networkx as nx

from transport_network import create_graph


def dfs_path(graph: nx.Graph, start: str, goal: str) -> Optional[List[str]]:
    stack: List[tuple[str, List[str]]] = [(start, [start])]
    visited: set[str] = set()

    while stack:
        node, path = stack.pop()
        if node in visited:
            continue

        visited.add(node)
        if node == goal:
            return path

        neighbors: Iterable[str] = graph.neighbors(node)
        for neighbor in reversed(list(neighbors)):
            if neighbor not in visited:
                stack.append((neighbor, path + [neighbor]))

    return None


def bfs_path(graph: nx.Graph, start: str, goal: str) -> Optional[List[str]]:
    queue: deque[tuple[str, List[str]]] = deque([(start, [start])])
    visited: set[str] = {start}

    while queue:
        node, path = queue.popleft()
        if node == goal:
            return path

        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return None


def format_path(path: Optional[List[str]]) -> str:
    if not path:
        return "шлях не знайдено"
    return " -> ".join(path)


def explain_difference(dfs: Optional[List[str]], bfs: Optional[List[str]]) -> str:
    if not dfs and not bfs:
        return "Жоден алгоритм не знайшов шлях між заданими узлами."
    if not dfs:
        return "DFS не знайшов шлях, тоді як BFS зміг його знайти завдяки повному пошуку в ширину."
    if not bfs:
        return "BFS не знайшов шлях, тоді як DFS знайшов його через глибокий обхід."

    dfs_edges = len(dfs) - 1
    bfs_edges = len(bfs) - 1

    explanation = [
        f"DFS пройшов шлях {format_path(dfs)}, роблячи пріоритет на першій гілці, яку зустрів.",
        f"BFS повернув маршрут {format_path(bfs)}, оскільки розширює фронт пошуку рівень за рівнем і знаходить шлях з мінімальною кількістю ребер.",
    ]

    if bfs_edges < dfs_edges:
        explanation.append(
            "BFS виявив коротший маршрут, тому що вже на другому рівні пошуку натрапив на вузол 'Lutsk', "
            "який безпосередньо веде до 'Lviv' і далі до 'Krakow'. DFS же спочатку проходить через 'Zhytomyr' "
            "та 'Vinnytsia', що додає зайві кроки перед досягненням мети."
        )
    elif bfs_edges > dfs_edges:
        explanation.append(
            "У цьому графі DFS випадково знайшов коротший шлях, бо перша досліджена гілка вже вела до цілі, "
            "тоді як BFS спершу перебрав інші рівні."
        )
    else:
        explanation.append(
            "Обидва алгоритми дають маршрути однакової довжини, однак вони можуть відрізнятися порядком відвідування вершин."
        )

    return "\n".join(explanation)


def main() -> None:
    graph = create_graph()
    start, goal = "Kyiv", "Krakow"

    dfs_result = dfs_path(graph, start, goal)
    bfs_result = bfs_path(graph, start, goal)

    print("DFS path:", format_path(dfs_result))
    print("BFS path:", format_path(bfs_result))
    print()
    print(explain_difference(dfs_result, bfs_result))


if __name__ == "__main__":
    main()

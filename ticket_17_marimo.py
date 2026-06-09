import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    mo.md("""# Дискретная математика. Билет 17 """)
    return (mo,)


@app.cell
def _():
    from collections import defaultdict, deque

    import matplotlib.pyplot as plt

    return defaultdict, deque, plt


@app.cell
def _(defaultdict):
    edges = [(1, 2), (1, 3), (2, 4), (3, 4)]

    graph = defaultdict(list)
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)

    for vertex in graph:
        graph[vertex].sort()
    return edges, graph


@app.cell
def _(edges, plt):
    pos = {
        1: (0, 1),
        2: (1.5, 1.8),
        3: (1.5, 0.2),
        4: (3, 1),
    }

    def path_edges(path):
        return {tuple(sorted((a, b))) for a, b in zip(path, path[1:])}

    def draw_graph(title, highlight=None, distances=None):
        active = path_edges(highlight or [])
        fig, ax = plt.subplots(figsize=(6, 3.5))

        for a, b in edges:
            x1, y1 = pos[a]
            x2, y2 = pos[b]
            edge = tuple(sorted((a, b)))
            color = "#d95f02" if edge in active else "#9aa0a6"
            width = 4 if edge in active else 2
            ax.plot([x1, x2], [y1, y2], color=color, linewidth=width, zorder=1)

        for v, (x, y) in pos.items():
            label = str(v)
            if distances and v in distances:
                label += f"\nd={distances[v]}"

            color = "#2e7d32" if v == 1 else "#6a1b9a" if v == 4 else "#1f77b4"
            ax.scatter(x, y, s=900, color=color, edgecolor="white", linewidth=2.5, zorder=2)
            ax.text(x, y, label, ha="center", va="center", color="white", fontsize=12, weight="bold")

        ax.set_title(title)
        ax.set_axis_off()
        ax.set_xlim(-0.4, 3.4)
        ax.set_ylim(-0.25, 2.25)
        plt.show()

    return (draw_graph,)


@app.cell
def _(draw_graph):
    draw_graph("Исходный граф")
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 1. **Backtracking**
    Идея:

    1. выбираем возможный шаг;
    2. добавляем его в текущее частичное решение;
    3. рекурсивно продолжаем поиск;
    4. после возврата отменяем выбор, чтобы попробовать другую ветку.
    """)
    return


@app.cell
def _(graph):
    def backtracking_paths(start, target):
        paths = []

        def backtrack(v, path, used):
            if v == target:
                paths.append(path[:])
                return

            for to in graph[v]:
                if to not in used:
                    used.add(to)
                    path.append(to)

                    backtrack(to, path, used)

                    path.pop()
                    used.remove(to)

        backtrack(start, [start], {start})
        return paths

    paths = backtracking_paths(1, 4)
    return (paths,)


@app.cell
def _(mo, paths):
    paths_text = "\n".join(f"- `{' -> '.join(map(str, path))}`" for path in paths)

    mo.md(
        f"""
        **Результат backtracking:**

        {paths_text}

        Значит, из `1` в `4` есть два простых пути.
        """
    )
    return


@app.cell
def _(draw_graph, paths):
    for path in paths:
        draw_graph(f"Путь backtracking: {' -> '.join(map(str, path))}", highlight=path)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 2. Кратчайшее расстояние
    **BFS** — Был выбран именно поиск в ширину, в невзвешенном графе он находит кратчайшее
    расстояние, потому что обходит вершины по слоям
    """)
    return


@app.cell
def _(deque, graph):
    def bfs_shortest_path(start, target):
        queue = deque([start])
        parent = {start: None}
        distance = {start: 0}

        while queue:
            v = queue.popleft()

            if v == target:
                break

            for to in graph[v]:
                if to not in distance:
                    distance[to] = distance[v] + 1
                    parent[to] = v
                    queue.append(to)

        if target not in distance:
            return -1, [], distance

        path = []
        v = target
        while v is not None:
            path.append(v)
            v = parent[v]

        return distance[target], path[::-1], distance

    shortest_distance, shortest_path, distances = bfs_shortest_path(1, 4)
    return distances, shortest_distance, shortest_path


@app.cell
def _(mo, shortest_distance, shortest_path):
    mo.md(f"""
    **Результат**
    - кратчайший путь: `{' -> '.join(map(str, shortest_path))}`;
    - кратчайшее расстояние от `1` до `4`: **{shortest_distance}**.

    Ответ: **2**.
    """)
    return


@app.cell
def _(distances, draw_graph, shortest_path):
    draw_graph("BFS: расстояния от вершины 1", highlight=shortest_path, distances=distances)
    return


if __name__ == "__main__":
    app.run()

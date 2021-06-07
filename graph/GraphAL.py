from collections import defaultdict


class GraphAL:
    def __init__(self):
        self.edges = defaultdict(set)
        self.vertices = set()

    def add_edge(self, u, v, w=0):
        self.edges[u].add((v, w))
        self.edges[v].add((u, w))
        self.vertices.add(u)
        self.vertices.add(v)

    def add_edges(self, u, sv, sw=None):
        if sw is None:
            sw = [0] * len(sv)
        for v, w in zip(sv, sw):
            self.add_edge(u, v, w)

    def complement(self):
        g = GraphAL()
        for u in self.edges:
            all_vertices = set(self.edges)
            all_vertices.remove(u)
            for v in self.edges[u]:
                all_vertices.remove(v)
            g.add_edges(u, all_vertices)
        return g

    def is_connected(self):
        if len(self.edges) < 1:
            return True
        visited = set()

        def visit(u):
            if u not in visited:
                visited.add(u)
                for v, w in self.edges[u]:
                    visit(v)

        visit(next(iter(self.edges)))
        return len(visited) == len(self.vertices)

    def is_bipartite(self):
        visited = defaultdict(bool)

        def color(u, c):
            visited[u] = c
            for v, w in self.edges[u]:
                if v in visited:
                    if visited[v] == visited[u]:
                        return False
                    continue
                if not color(v, not c):
                    return False
            return True

        for u in self.edges:
            if u not in visited:
                if not color(u, True):
                    return False
        return True

    @staticmethod
    def find(u, sets):
        for s in sets:
            if u in s:
                return s
        return None

    def has_cycle(self):
        set_of_vertices = self.vertices.copy()
        set_of_edges = set(
            (u, v, w) for u in self.edges for v, w in self.edges[u] if u < v
        )
        subgraphs = list()
        for u, v, w in sorted(set_of_edges, key=lambda x: x[2]):
            su = GraphAL.find(u, subgraphs)
            sv = GraphAL.find(v, subgraphs)
            if su is None and sv is None:
                subgraphs.append({u, v})
                set_of_vertices.remove(u)
                set_of_vertices.remove(v)
            elif su == sv:
                return True
            elif su is None:
                sv.add(u)
            elif sv is None:
                su.add(v)
            else:
                su.update(sv)
                subgraphs.remove(sv)
        return False

    def minimum_spanning_tree_prim(self):
        g = GraphAL()
        if not self.is_connected():
            return g
        start_vertex = next(iter(self.vertices))
        set_of_edges = {(u, v, w) for u in self.edges for v, w in self.edges[u] if u < v}
        edges_to_consider = {(u, v, w) for u, v, w in set_of_edges if start_vertex in (u, v)}
        visited = {start_vertex}
        while len(visited) != len(self.vertices):
            min_weighted_edge = min(edges_to_consider, key=lambda x: x[2])
            start_vertex = (
                min_weighted_edge[1]
                if min_weighted_edge[0] in visited
                else min_weighted_edge[0]
            )
            visited.add(start_vertex)
            edges_to_consider.update(
                (u, v, w) for u, v, w in set_of_edges if start_vertex in (u, v)
            )
            edges_to_consider.remove(min_weighted_edge)
            g.add_edge(*min_weighted_edge)
        return g

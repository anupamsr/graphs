from collections import defaultdict


class GraphAL:
    def __init__(self):
        self.edges = defaultdict(set)
        self.vertices = set()

    def add_edge(self, u, v, w=1):
        self.edges[u].add((v, w))
        self.edges[v].add((u, w))
        self.vertices.add(u)
        self.vertices.add(v)

    def add_edges(self, u, sv, sw=None):
        if sw is None:
            for v in sv:
                self.add_edge(u, v)
        else:
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

        def color(vertex, c):
            visited[vertex] = c
            for v, w in self.edges[vertex]:
                if v in visited:
                    if visited[v] == visited[vertex]:
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

    def has_cycle(self):
        set_of_edges = set((u, v, w) for u in self.edges for v, w in self.edges[u] if u < v)
        set_of_vertices = list()

        def find_set_of_vertices(vertex):
            for s in set_of_vertices:
                if vertex in s:
                    return s

        for u, v, w in sorted(set_of_edges, key=lambda x: x[2]):
            su = find_set_of_vertices(u)
            sv = find_set_of_vertices(v)
            if su is None and sv is None:
                set_of_vertices.append({u, v})
            elif su == sv:
                return True
            elif su is None:
                sv.add(u)
            elif sv is None:
                su.add(v)
            else:
                su.update(sv)
                set_of_vertices.remove(sv)
        return False

    def minimum_spanning_tree_prim(self):
        g = GraphAL()
        if not self.is_connected():
            return g
        current_vertex = next(iter(self.vertices))
        visited = {current_vertex}
        unique_edges = {(u, v, w) for u in self.edges for v, w in self.edges[u] if u < v}
        edges_to_consider = {(u, v, w) for u, v, w in unique_edges if current_vertex in (u, v)}
        while len(visited) != len(self.vertices):
            min_weighted_edge = min(edges_to_consider, key=lambda x: x[2])
            current_vertex = next(filter(lambda x: x not in visited, min_weighted_edge[:2]), None)
            if current_vertex is not None:
                g.add_edge(*min_weighted_edge)
                visited.add(current_vertex)
                edges_to_consider.update(
                    (u, v, w) for u, v, w in unique_edges if current_vertex in (u, v)
                )
            edges_to_consider.remove(min_weighted_edge)
        return g

    def minimum_spanning_tree_kruskal(self):
        set_of_edges = list()

        def find_set_of_edges(vertex):
            for s in set_of_edges:
                for e in s:
                    if vertex in e[:2]:
                        return s
            return None

        unique_edges = {(u, v, w) for u in self.edges for v, w in self.edges[u] if u < v}
        while len(unique_edges) > 0:
            min_weighted_edge = min(unique_edges, key=lambda x: x[2])
            unique_edges.remove(min_weighted_edge)
            su = find_set_of_edges(min_weighted_edge[0])
            sv = find_set_of_edges(min_weighted_edge[1])
            if su is None and sv is None:
                set_of_edges.append({min_weighted_edge})
            elif su is None:
                sv.add(min_weighted_edge)
            elif sv is None:
                su.add(min_weighted_edge)
            elif su != sv:
                sv.add(min_weighted_edge)
                su.update(sv)
                set_of_edges.remove(sv)

        gmsts = list()
        for s in set_of_edges:
            g = GraphAL()
            for e in s:
                g.add_edge(*e)
            gmsts.append(g)
        return gmsts

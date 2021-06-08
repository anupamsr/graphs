from graph import GraphAL
import networkx as nx
import matplotlib.pyplot as plt


def draw_with_kruskal_mst(g: GraphAL):
    if len(g.edges) == 0:
        return
    nxg = nx.Graph()
    unique_edges = [(u, v, w) for u in g.edges for v, w in g.edges[u] if u < v]
    gmsts = g.minimum_spanning_tree_kruskal()
    mst_edges = [(u, v, w) for gmst in gmsts for u in gmst.edges for v, w in gmst.edges[u] if u < v]
    print(mst_edges)
    list(map(unique_edges.remove, mst_edges))
    nxg.add_weighted_edges_from(unique_edges, color="black")
    nxg.add_weighted_edges_from(mst_edges, color="red")
    colors = nx.get_edge_attributes(nxg, "color").values()
    weights = nx.get_edge_attributes(nxg, "weight").values()
    options = {
        "node_color": "lightblue",
        "edge_color": colors,
        "width": list(weights),
        "with_labels": True,
    }
    if g.is_bipartite():
        pos = nx.drawing.layout.bipartite_layout(nxg, nx.bipartite.sets(nxg)[0])
    else:
        try:
            pos = nx.planar_layout(nxg)
        except nx.NetworkXException:
            pos = None
    nx.draw(nxg, pos=pos, **options)
    plt.show()


def print_info(g: GraphAL):
    print("Edges:", g.edges)
    print("Vertices:", g.vertices)
    print("is connected", g.is_connected())
    print("is bipartite:", g.is_bipartite())
    print("has cycle:", g.has_cycle())
    print("mst by prim", g.minimum_spanning_tree_prim().edges)
    draw_with_kruskal_mst(g)


def main():
    g1 = GraphAL()
    g1.add_edges(0, [1, 7])
    g1.add_edges(1, [2, 7])
    g1.add_edges(2, [8, 5, 3])
    g1.add_edges(3, [5, 4])
    g1.add_edge(4, 5)
    g1.add_edge(5, 6)
    g1.add_edges(6, [8, 7])
    g1.add_edge(7, 8)
    print_info(g1)
    g2 = GraphAL()
    g2.add_edges(1, [2, 3])
    g2.add_edges(4, [2, 3])
    g2.add_edges(5, [2, 7, 6])
    g2.add_edges(8, [6, 7])
    print_info(g2)
    g3 = GraphAL()
    g3.add_edges(1, [2, 3])
    print_info(g3)
    g3.add_edges(4, [2, 3])
    print_info(g3)
    g3.add_edges(5, [6, 7])
    g3.add_edges(6, [5, 7])
    print_info(g3)
    g4 = GraphAL()
    g4.add_edges(1, [2, 6], [28, 10])
    g4.add_edges(2, [7, 3], [14, 16])
    g4.add_edge(3, 4, 12)
    g4.add_edges(4, [7, 5], [18, 22])
    g4.add_edges(5, [6, 7], [25, 24])
    print_info(g4)
    g5 = GraphAL()
    g5.add_edge(1, 2, 10)
    g5.add_edge(2, 3, 11)
    g5.add_edge(3, 4, 20)
    g5.add_edge(4, 2, 13)
    print_info(g5)
    petersen = GraphAL()
    petersen.add_edges(1, [3, 4, 6])
    petersen.add_edges(2, [4, 5, 7])
    petersen.add_edges(3, [5, 1, 8])
    petersen.add_edges(4, [1, 2, 9])
    petersen.add_edges(5, [2, 3, 10])
    petersen.add_edges(6, [1, 7, 10])
    petersen.add_edges(7, [2, 6, 8])
    petersen.add_edges(8, [3, 7, 9])
    petersen.add_edges(9, [4, 8, 10])
    petersen.add_edges(10, [5, 9, 6])
    print_info(petersen)


if __name__ == "__main__":
    main()

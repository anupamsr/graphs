from graph import GraphAL


def print_info(g: GraphAL):
    print(g.edges)
    print(g.vertices)
    print("is connected", g.is_connected())
    print("is bipartite:", g.is_bipartite())
    print("has cycle:", g.has_cycle())
    print(g.minimum_spanning_tree_prim().edges)


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


if __name__ == "__main__":
    main()

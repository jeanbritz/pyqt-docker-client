
class Vertex:

    def __init__(self, name="New"):
        self.name = name
        self.neighbours = []

    def connect(self, vertex):
        if vertex not in self.neighbours:
            self.neighbours.append(vertex)
            vertex.connect(self)

    def get_degree(self):
        return len(self.neighbours)

    def __str__(self):
        return self.name

    def get_neighbours(self):
        rs = ""
        for n in self.neighbours:
            rs = rs + "-" + str(n)
        return rs

def get_graph_size():
    pass


def main():
    print("App started")
    a = Vertex("A")
    b = Vertex("B")
    c = Vertex("C")
    d = Vertex("D")
    e = Vertex("E")

    a.neighbours = []
    b.neighbours = []
    c.neighbours = []
    d.neighbours = []
    e.neighbours = []

    a.connect(b)
    a.connect(c)
    a.connect(d)
    a.connect(e)

    b.connect(c)
    d.connect(c)
    e.connect(c)

    print("A connects to " + a.get_neighbours())
    print("B connects to " + b.get_neighbours())
    print("C connects to " + c.get_neighbours())
    print("D connects to " + d.get_neighbours())
    print("E connects to " + e.get_neighbours())


class Node:

    def __init__(self, name=None):
        self.name = name;

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'{self.name}'


def build_graph():
    graph = {}
    A = Node("A")
    B = Node("B")
    C = Node("C")
    D = Node("D")
    E = Node("E")
    F = Node("F")

    node_list = [C]
    graph[A] = node_list
    node_list = [C, E]
    graph[B] = node_list
    node_list = [A, B, D, E]
    graph[C] = node_list
    node_list = [C]
    graph[D] = node_list
    node_list = [C, B]
    graph[E] = node_list
    graph[F] = []
    return graph


def generate_edges(graph):
    edges = []
    for node in graph:
        for neighbour in graph[node]:
            edges.append((node, neighbour))
    return edges


if __name__ == "__main__":
    graph = build_graph()
    print(graph)
    edges = generate_edges(graph)
    print(edges)

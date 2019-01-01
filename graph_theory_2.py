

class Graph(object):

    def __init__(self, graph_dict=None):
        """
        Initialises a graph object
        """
        if graph_dict is None:
            graph_dict = {}
        self.__graph_dict = graph_dict

    def list_vertices(self):
        """
        Returns the vertices of the graph
        """
        return list(self.__graph_dict.keys());

    def list_edges(self):
        """
        Returns the edges of the graph
        """
        return self.__generate_edges()

    def __generate_edges(self):
        """ A static method generating the edges of the
                    graph "graph". Edges are represented as sets
                    with one (a loop back to the vertex) or two
                    vertices
                """
        edges = []
        for vertex in self.__graph_dict:
            for neighbour in self.__graph_dict[vertex]:
                edges.append({vertex, neighbour})
        return edges

    def add_vertex(self, vertex):
        """
        If the vertex "vertex" is not in
        self.__graph_dict, a key "vertex" with an empty
        list as a value is added to the dictionary.
        Otherwise nothing has to be done.
        """
        if vertex not in self.__graph_dict:
            self.__graph_dict[vertex] = []

    def add_edge(self, edge):
        """
        Assumes that edge is of type set, tuple or list;
        between two vertices can be multiple edges!
        """
        edge = set(edge)
        (vertex1, vertex2) = tuple(edge)
        if vertex1 in self.__graph_dict:
            self.__graph_dict[vertex1].append(vertex2)
        else:
            self.__graph_dict[vertex1] = [vertex2]

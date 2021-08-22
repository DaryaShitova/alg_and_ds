from Vertex import My_Vertex
from Edge import My_Edge


class Graph():
    def __init__(self):
        self.vertices = []  # list of vertices in the graph
        self.edges = []     # list of edges in the graph
        self.num_vertices = 0
        self.num_edges = 0
        self.undirected_graph = True

    def double_array_size(self):
        self.vertices = self.vertices.copy() + [My_Vertex()] * len(self.vertices) * 2
        self.edges = self.edges.copy() + [My_Edge()] * len(self.edges) * 2 * (len(self.edges) * 2 -1)

    def get_number_of_vertices(self):
        """return: the number of vertices in the graph
        """
        return self.num_vertices

    def get_number_of_edges(self):
        """return: the number of edges in the graph
        """
        return self.num_edges

    def get_vertices(self):
        """return: array of length get_number_of_vertices() with the vertices in the graph
        """
        return self.vertices

    def get_edges(self):
        """return: array of length get_number_of_edges() with the edges in the graph
        """
        return self.edges

    def insert_vertex(self, vertex):
        """Inserts a new vertex into the graph and returns its index in the vertex array.
	    If the vertex array is already full, then the method double_array_size() shall be called
	    before inserting.
        None parameter is not allowed (ValueError).
        :param vertex: the vertex to be inserted
        :return: index of the new vertex in the vertex array
        :raises: ValueError if any of the parameters is None
        """
        if vertex is None:
            raise ValueError("Vertex is None")

        self.vertices.append(vertex)
        self.num_vertices += 1
        return self.num_vertices-1

    def has_edge(self, vertex1, vertex2):
        """Returns the edge weight if there is an edge between index vertex1 and vertex2, otherwise -1.
	    In case of unknown or identical vertex indices raise a ValueError.
        :param vertex1: first vertex
        :param vertex2: second vertex
        :return: edge weight of -1 if there is no edge
        :raises: ValueError if any of the parameters is None
        """
        if vertex1 is None or vertex2 is None or vertex1==vertex2:
            raise ValueError("One of the parameters is None or equal to the other.")

        #Checking if there is an edge with the provided vertices
        for edge in self.edges:
            if edge.vertex_in == vertex1 and edge.vertex_out == vertex2:
                return edge.weight

        return -1

    def insert_edge(self, vertex1, vertex2, weight):
        """Inserts an edge between vertices with index of vertex1 and index of vertex2. False is returned if the edge already exists,
	    True otherwise. A ValueError shall be raised if the vertex indices are unknown (out of range) or
	    if v1 == v2 (loop).
        .
        .
        :param vertex1: first index of vertex
        :param vertex2: second index of vertex
        :param weight: weight of the edge
        :return: True if the edge could be created, False otherwise
        :raises: ValueError if any of the parameters is None any of the vertices is out of range
        """
        if vertex1 is None or vertex2 is None or weight is None or vertex1 >= self.num_vertices \
                or vertex2 >= self.num_vertices or vertex2==vertex1:
            raise ValueError("One of the parameters is None, out of range or vertex1 is equal to vertex2")

        #Chcking if the edge already exists. If yes, returning False, otherwise creating a new edge and inserting it.
        edge_check = self.has_edge(vertex1, vertex2)
        if edge_check != -1:
            return False
        else:
            edge_to_insert = My_Edge()
            edge_to_insert.vertex_in = vertex1
            edge_to_insert.vertex_out = vertex2
            edge_to_insert.weight = weight

            self.edges.append(edge_to_insert)
            self.num_edges += 1
            return True


    def get_adjacency_matrix(self):
        """Returns an NxN adjacency matrix for the graph, where N = get_number_of_vertices().
        The matrix contains 1 if there is an edge at the corresponding index position, otherwise 0.
        :return: NxN adjacency matrix
        """
        #Creating an NxN adjacency matrix for the graph with all zeros
        adjacency_matrix = []
        for i in range(self.get_number_of_vertices()):
            adjacency_matrix.append([0 for i in range(self.get_number_of_vertices())])

        #Checking each pair of of vertices if they are connected by an edge. If yes, changing the zero in the matrix to one.
        for i in range(self.get_number_of_vertices()):
            for j in range(self.get_number_of_vertices()):
                if i != j:
                    edge_to_check = self.has_edge(j,i)
                else:
                    edge_to_check = -1
                if edge_to_check != -1:
                    adjacency_matrix[i][j] = 1
                    adjacency_matrix[j][i] = 1
        return adjacency_matrix


    def get_adjacent_vertices(self, vertex):
        """Returns an array of vertices which are adjacent to the vertex with index "vertex".
        :param vertex: The vertex of which adjacent vertices are searched.
        :return: array of adjacent vertices to "vertex".
        :raises: ValueError if the vertex index "vertex" is unknown
        """
        if vertex is None:
            raise ValueError("Vertex is unknown")

        index = self.vertex_search(vertex)

        if index == -1:
            raise ValueError("Vertex is not found")
        else:
            adjacent_matrix = self.get_adjacency_matrix()
            adjacent_vertices = []
            #Checking what adjacent vertices the provided vertex has in the adjacent matrix.
            for counter, i in enumerate(adjacent_matrix[index]):
                if i == 1:
                    adjacent_vertices.append(self.vertices[counter])
            return adjacent_vertices


    # ------------- """Example 2""" -------------

    def is_connected(self):
        """return: True if the graph is connected, otherwise False.
        """
        #Creating a list to keep track of the visited vertices.
        visited_vertices = [False]*self.get_number_of_vertices()
        self.DFS(self.vertices[0], visited_vertices)
        #Checking if every of the vertices has been visited.
        for v in visited_vertices:
            if v is False:
                return False
        return True

    def get_number_of_components(self):
        """return: The number of all (weak) components
        """
        #Creating a list to keep track of the visited vertices.
        visited_vertices = [False]*self.get_number_of_vertices()
        #Counter of the components.
        count = 0

        for v in range(self.get_number_of_vertices()):
            #Checking if any of the vertices is still not visited. If yes, adding one to the counter.
            if visited_vertices[v] == False:
                self.DFS(self.vertices[v], visited_vertices)
                count += 1
        return count

    def print_components(self):
        """Prints the vertices of all components (one line per component).
        E.g.: A graph with 2 components (first with 3 vertices, second with 2 vertices) should look like:
   	 	[vertex1] [vertex2] [vertex3]
   	    [vertex4] [vertex5]
        """
        #Creating a list to keep track of the visited vertices.
        visited_vertices = [False] * self.get_number_of_vertices()

        for v in range(self.get_number_of_vertices()):
            #Creating a list for each of the components and printing elements of each in a line.
            if visited_vertices[v] == False:
                temp = []
                self.print_helper(temp, self.vertices[v], visited_vertices)
                print("[" + "] [".join(temp[:]) +"]")

    def is_cyclic(self):
        """return: Returns True if the graphs contains cycles, otherwise False.
        """
        # Creating a list to keep track of the visited vertices.
        visited_vertices = [False]*self.get_number_of_vertices()
        #Checking each of the vertices (if it has not been changed to True yet) using the helper function.
        for v in range(self.get_number_of_vertices()):
            if visited_vertices[v]==False:
                if self.is_cyclic_helper(self.vertices[v],visited_vertices,-1) == True:
                    return True
        return False

    """
    Helper functions
    """

    def vertex_search(self,vertex):
        """Searches for the provided vertex in the vertices list and returns the index and -1 if the vertex was not found"""
        index = -1
        for i in range(self.get_number_of_vertices()):
            if self.vertices[i] == vertex:
                index = i
        return index


    def DFS(self, vertex, visited_vertices):
        """Perform DFS search"""
        i = self.vertex_search(vertex)
        #Marking current node as visited
        visited_vertices[i] = True

        #Checking the adjacent vertices of the provided vertex and applying the DFS on them recursively if they have not been visited yet.
        for v in self.get_adjacent_vertices(vertex):
            index = self.vertex_search(v)
            if not visited_vertices[index]:
                self.DFS(v, visited_vertices)

    def is_cyclic_helper(self, vertex, visited_vertices, parent):
        """Helper function of is_cyclic"""
        i = self.vertex_search(vertex)
        # Marking current node as visited
        visited_vertices[i] = True
        for v in self.get_adjacent_vertices(vertex):
            index = self.vertex_search(v)
            #If the vertex has not been visited it, continue checking recursively
            if visited_vertices[index]==False:
                if self.is_cyclic_helper(v, visited_vertices,i):
                    return True
            #If an adjacent vertex has been visited and it is not a previous vertex, return True.
            elif parent != index:
                return True
        return False


    def print_helper(self, temp, vertex, visited_vertices):
        """Helper function of print_components"""
        i = self.vertex_search(vertex)
        #Marking current node as visited
        visited_vertices[i] = True
        #Appending the vertex to the list to be printed
        temp.append(self.vertices[i].name)

        for v in self.get_adjacent_vertices(vertex):
            index = self.vertex_search(v)
            #Recursively taking the vertices that has not been checked yet.
            if not visited_vertices[index]:
                temp=self.print_helper(temp, v, visited_vertices)
        return temp

#Resources used:
#https://www.techiedelight.com/check-given-graph-strongly-connected-not/
#https://medium.com/analytics-vidhya/graphs-in-python-adjacency-matrix-d0726620e8d7
#https://www.geeksforgeeks.org/detect-cycle-undirected-graph/
#https://www.geeksforgeeks.org/program-to-count-number-of-connected-components-in-an-undirected-graph/
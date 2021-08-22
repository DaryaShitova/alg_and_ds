from Graph import Graph
import math


class Roadmap(Graph):
    def __init__(self):
        super().__init__()

    def print_shortest_distance(self, from_station: int, to_station: int):
        """This method determines and prints the shortest path between two stations (= vertex indices) "from_station" and "to_station",
       	 using the dijkstra algorithm. The shortest distance is returned.
       	 @param from_station
       	 	vertex index of the start station
       	 @param to_station
       	 	vertex index of the destination station
       	 @return
       	    The path with the already covered distance is returned as List of tuples. This list contains sequentially
       	    each station's name along the shortest path, together with the already covered distance.
       	    (see example on the assignment sheet)
    	 """
        #To keep track of already checked stations
        visited = [False for i in range(self.get_number_of_vertices())]
        #List of currently known distances from the start station
        distance = self.get_weighted_adjacency_matrix()[from_station]

        cur = from_station
        i = 0
        #To keep track of parent vertices
        parent = [-1 for i in range(self.get_number_of_vertices())]

        #Checking the shortest distance and updating the parent list if the shortest distance has been updated
        while False in visited and i < self.get_number_of_vertices():
            cur, visited, distance, index_list = self.dijkstra_shortest_path(cur, visited, distance)
            i += 1
            for j in index_list:
                parent[j] = cur

        start_station = self.get_vertices()[from_station]
        start_name = start_station.name

        path = [(start_name,0)]
        self.append_to_path(parent, to_station, path, distance)
        print("Shortest distance from " + path[0][0] + " to "+path[-1][0] + ":", distance[to_station])
        for i in path[1:-1]:
            print("   over " + i[0] + ":", i[1])
        print("   to " + path[-1][0] + ":", path[-1][1])
        return path

    def print_shortest_distances(self, from_station: int):
        """This method determines and prints the shortest path from station (= vertex index) "from_station" to all other stations
       	 using the dijkstra algorithm, and returns them in a list.
       	 @param from_station
       	 	vertex index of the start station
       	 @return:
       	 	the results in form of a list of integers, where the indices correspond to the indices of the stations.
       	    (see example on the assignment sheet)
        """
        # To keep track of already checked stations
        visited = [False for i in range(self.get_number_of_vertices())]
        # List of currently known distances from the start station
        distance = self.get_weighted_adjacency_matrix()[from_station]

        cur = from_station
        i = 0
        # Checking the shortest distance
        while False in visited and i < self.get_number_of_vertices():
            cur, visited, distance, _ = self.dijkstra_shortest_path(cur,visited,distance)
            i += 1

        for i in range(self.get_number_of_vertices()):
            if distance[i] == math.inf:
                distance[i] = -1

        start_station = self.get_vertices()[from_station]
        start_name = start_station.name
        print("from " + start_name)
        for i in range(len(distance)):
            station = self.get_vertices()[i]
            station_name = station.name
            print("   to " + station_name + ":", distance[i])
        return distance

    def dijkstra_shortest_path(self, cur: int, visited, distance):
        visited[cur] = True
        index_list = [] #to keep track of the updated distance to update the parent

        cur_distance = distance.copy()
        for i in range(len(cur_distance)):
            if visited[i] == True:
                cur_distance[i] = math.inf

        min_ver = cur_distance.index(min(cur_distance))
        distance_min_ver = self.get_weighted_adjacency_matrix()[min_ver]

        #Updating the distance if the new found distance is shorted than the one already in the list
        for i in range(len(distance)):
            if (distance[min_ver]+distance_min_ver[i]) < distance[i]:
                distance[i] = (distance[min_ver]+distance_min_ver[i])
                index_list.append(i)
        return min_ver, visited, distance, index_list


    def append_to_path(self, parent, i, path, distance):
        # Recursively appends the stations to the shortest path.
        if parent[i] == -1:
            station = self.get_vertices()[i]
            path.append((station.name, distance[i]))
            return path
        self.append_to_path(parent, parent[i], path, distance)
        station = self.get_vertices()[i]
        path.append((station.name, distance[i]))

#Resources used to solve the exercise:
#https://www.geeksforgeeks.org/printing-paths-dijkstras-shortest-path-algorithm/
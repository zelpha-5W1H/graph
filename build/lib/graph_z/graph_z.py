import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

sns.set_theme(style='darkgrid')

def get_distance(p1, p2):
    return np.sqrt(sum([(p2_coordinate - p1_coordinate) ** 2 for p1_coordinate, p2_coordinate in zip(p1, p2)]))

def get_midpoint(p1, p2):
    return ((p1[0]+p2[0])/2, (p1[1]+p2[1])/2)


def plot_line_segment(p1, p2, scaling_factor=1):
    L = get_distance(p1, p2)
    p2_m = ((p1[0]*(1-scaling_factor) + p2[0]*scaling_factor), (p1[1]*(1-scaling_factor) + p2[1]*scaling_factor))
    plt.arrow(p1[0], p1[1], p2_m[0], p2_m[1], head_width=0, color='black')

class Vertex():
    def __init__(self, id, value, paths=None):
        self.id = id
        self.value = value
        self.paths = paths or []

class Graph:
    def __init__(self, vertices=[]):
        self.vertices = vertices
        self.ids = []
        self.all_paths = []
        for vertex in vertices:
            self.ids.append(vertex.id)
            for path in vertex.paths:
                full_path = (vertex.id, path[0], path[1])
                if full_path not in self.all_paths:
                    self.all_paths.append(full_path)
    

    def add_vertex(self, vertex):
        if vertex.id in self.ids:
            print("Please enter an unique ID")
            return None
        self.vertices.append(vertex)
        self.ids.append(vertex.id)

    def get_vertex(self, id):
        for vertex in self.vertices:
            if vertex.id == id:
                return vertex

    def add_path(self, id1, id2, path_cost, message=True):
        if id1 not in self.ids or id2 not in self.ids:
            print("Vertices with the given ids do not exist in this graph")
            return None

        vertex1, vertex2 = self.get_vertex(id1), self.get_vertex(id2)
        existance_of_copy = False
        for i, path in enumerate(self.all_paths):
            if (path[0] == id1 and path[1] == id2) or (path[0] == id2 and path[1] == id1):
                existance_of_copy = True
                self.all_paths[i] = (id1, id2, path_cost)
                previous_cost = path[2]
                break
        if existance_of_copy:
            vertex1.paths[vertex1.paths.index((id2, previous_cost))] = (id2, path_cost)
            vertex2.paths[vertex2.paths.index((id1, previous_cost))] = (id1, path_cost)
        else:
            self.all_paths.append((id1, id2, path_cost))
            vertex1.paths.append((id2, path_cost))
            vertex2.paths.append((id1, path_cost))
        if message:
            print("Path added succesfully")


    def bar_visuals(self):
        values = [vertex.value for vertex in self.vertices]
        sns.barplot(pd.DataFrame({
            'IDs': self.ids,
            'Values': values
        }), x='IDs', y='Values')


    def plot_graph(self, show_path=True, specific_paths=None):
        fig, ax = plt.subplots()
        ax.set_aspect('equal')

        num_vertices = len(self.vertices)
        extras = num_vertices%4
        theta = np.linspace(0, 2*np.pi, num_vertices, endpoint=False)
        x = np.cos(theta)
        y = np.sin(theta)
                        
        # Plot the vertices
        ax.scatter(x, y)
        for i, vertex in enumerate(self.vertices):
            ax.annotate(f"{vertex.id}:{vertex.value}", (x[i], y[i]))

        paths_to_be_plotted = []
        if specific_paths == None:
            paths_to_be_plotted = self.all_paths
        else:
            for path in self.all_paths:
                if ((path[0], path[1]) in specific_paths) or ((path[1], path[0]) in specific_paths):
                    paths_to_be_plotted.append(path)

        if show_path:
            # Plot the edges
            for id1, id2, cost in paths_to_be_plotted:
                vertex1, vertex2 = self.get_vertex(id1), self.get_vertex(id2)
                i1, i2 = self.ids.index(id1), self.ids.index(id2)
                ax.plot([x[i1], x[i2]], [y[i1], y[i2]], color='black')
                ax.annotate(cost, ((x[i1]+x[i2])/2, (y[i1]+y[i2])/2))

        plt.show()        

    def get_path_length(self, id1, id2):
        for path in self.all_paths:
            if (path[0] == id1 and path[1] == id2) or (path[0] == id2 and path[1] == id1):
                return path[2]
        print("No path exists between the vertices of id(s) {} and {}".format(id1, id2))

    def get_detailed_dataframe(self):
        values = []
        paths = []
        for vertex in self.vertices:
            values.append(vertex.value)
            paths.append(vertex.paths)
        return pd.DataFrame({
            "IDs": self.ids,
            "Values": values,
            "Paths (id, cost)": paths,
        })

    def get_least_path_cost(self, id1, id2, plot=True):
        if id1 not in self.ids or id2 not in self.ids:
            print("The given IDs are invalid")
            return None
        

        distances = [(id, 2**16, id1) for id in self.ids]

        def get_dist(id):
            for dist in distances:
                if dist[0] == id:
                    return dist

        def update_dist(new_dist):
            for i in range(len(distances)):
                if distances[i][0] == new_dist[0]:
                    distances[i] = new_dist

        update_dist((id1, 0, id1))

        explored = []
        def get_least():
            least = 2**16 + 1
            id_of_the_least = None
            for dist in distances:
                if (dist[0] not in explored) and (dist[1] < least):
                    least = dist[1]
                    id_of_the_least = dist[0]          
            return id_of_the_least
        
        def get_distance(id):
            for dist in distances:
                if dist[0] == id:
                    return dist[1]
        
        while(get_least() != None):
            id = get_least()
            explored.append(id)
            for path in self.get_vertex(id).paths:
                # print(get_distance(id), get_distance(path[0]), path)
                potentially_new_distance = get_distance(id) + path[1]
                if potentially_new_distance < get_distance(path[0]):
                    update_dist((path[0], potentially_new_distance, id))

        if plot:
            selected_paths = []
            id = id2
            while(id != id1):
                next_id = get_dist(id)[2]
                selected_paths.append((id, next_id))
                id = next_id

        self.plot_graph(specific_paths=selected_paths)
        
        return get_distance(id2)



def generate_random_graph(num_vertices, num_paths=0, value_range=(0, 10), path_cost_range=(1, 10), random_ids=False):

    vertex_values = np.random.randint(*value_range, size=num_vertices)
    if random_ids:
        vertex_ids = np.random.randint(0, 2**16, size=num_vertices)
    else:
        vertex_ids = np.arange(1, num_vertices+1, 1)
    
    graph = Graph()
    for i in range(num_vertices):
        vertex = Vertex(vertex_ids[i], vertex_values[i])
        graph.add_vertex(vertex)
    
    path_costs = np.random.randint(*path_cost_range, size=num_paths)
    for i in range(num_paths):
        vertex_ids = [v.id for v in graph.vertices]  # get list of vertex IDs in the graph
        rand_id1, rand_id2 = np.random.choice(vertex_ids, size=2, replace=False)
        graph.add_path(rand_id1, rand_id2, path_costs[i], message=False)
    
    return graph


    

    





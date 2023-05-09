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
        self.circle_coordinates = (0, 0)

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

    def add_path(self, id1, id2, path_cost):
        if id1 not in self.ids or id2 not in self.ids:
            print("Vertices with the given ids do not exist in this graph")
            return None

        vertex1, vertex2 = self.get_vertex(id1), self.get_vertex(id2)
        existance_of_copy = False
        for i, path in enumerate(self.all_paths):
            if path[0] == id1 and path[1] == id2:
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

        print("Path added succesfully")


    def bar_visuals(self):
        values = [vertex.value for vertex in self.vertices]
        sns.barplot(pd.DataFrame({
            'IDs': self.ids,
            'Values': values
        }), x='IDs', y='Values')


    def plot_graph(self):
        fig, ax = plt.subplots()
        ax.set_aspect('equal')

        n = len(self.vertices)
        theta = np.linspace(0, 2*np.pi, n, endpoint=False)
        x, y = np.cos(theta), np.sin(theta)

        # Plot the vertices
        ax.scatter(x, y)
        for i, vertex in enumerate(self.vertices):
            ax.annotate(f"{vertex.id}:{vertex.value}", (x[i], y[i]))

        # Plot the edges
        for id1, id2, cost in self.all_paths:
            vertex1, vertex2 = self.get_vertex(id1), self.get_vertex(id2)
            i1, i2 = self.ids.index(id1), self.ids.index(id2)
            ax.plot([x[i1], x[i2]], [y[i1], y[i2]])
            ax.annotate(cost, ((x[i1]+x[i2])/2, (y[i1]+y[i2])/2))

        plt.show()

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







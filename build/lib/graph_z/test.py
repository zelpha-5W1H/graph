from graph_z import (
    generate_random_graph
)

g = generate_random_graph(18, 30, (3, 12), (1, 10))
print(g.get_detailed_dataframe())
g.plot_graph()
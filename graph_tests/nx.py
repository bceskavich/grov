import networkx as nx
from networkx.readwrite import json_graph
import json

dg = nx.DiGraph()
dg.add_edge('a', 'b')
dg.add_edge('a', 'c')
dg.add_edge('a', 'd')
dg.add_edge('b', 'a')
dg.add_edge('b', 'c')

graph = json_graph.dumps(dg, indent=1)
print graph
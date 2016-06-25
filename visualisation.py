import networkx as nx
from dataloader import load_connections, _DATA_PATH, _lang_indexes

_GRAPHHML_PATH = _DATA_PATH + "graphml/"

def save_graph(lang):
    connections = load_connections(lang)
    G = nx.Graph()
    G.add_edges_from(connections)
    nx.write_graphml(G,'%s%s_connections.graphml' % (_GRAPHHML_PATH, lang))


if __name__ == "__main__":
    for lang in _lang_indexes.keys():
        save_graph(lang)

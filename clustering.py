from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import os
import networkx as nx

CALL_GRAPH_FILE = "call_graph.gml"

def generate_or_load_call_graph(function_list_path):
    """
    Generate or load the static call graph.

    Args:
        function_list_path (str): Path to the file containing all functions.

    Returns:
        networkx.DiGraph: The call graph.
    """
    # Check if the call graph file exists
    if os.path.exists(CALL_GRAPH_FILE):
        print("Loading call graph from file...")
        return nx.read_gml(CALL_GRAPH_FILE)

    print("Generating new call graph...")
    G = nx.DiGraph()

    # Load all functions
    with open(function_list_path, "r") as f:
        all_functions = [line.strip() for line in f.readlines()]

    # Add nodes for all functions
    G.add_nodes_from(all_functions)

    # Generate edges (this should ideally be based on real relationships)
    for func in all_functions:
        num_edges = min(2, len(all_functions) - 1)  # Limit to max 2 edges per node
        for i in range(num_edges):
            target = all_functions[(all_functions.index(func) + i + 1) % len(all_functions)]
            G.add_edge(func, target)

    # Save the graph to file
    nx.write_gml(G, CALL_GRAPH_FILE)
    print(f"Call graph saved to {CALL_GRAPH_FILE}")
    return G

def update_call_graph(call_graph, uncovered_functions_path):
    """
    Update the call graph with uncovered function information.

    Args:
        call_graph (networkx.DiGraph): The call graph.
        uncovered_functions_path (str): Path to the file containing uncovered functions.

    Returns:
        networkx.DiGraph: The updated call graph.
    """
    # Load uncovered functions
    with open(uncovered_functions_path, "r") as f:
        uncovered_functions = {line.strip() for line in f.readlines()}

    # Update node attributes
    nx.set_node_attributes(call_graph, False, "uncovered")
    for func in uncovered_functions:
        if func in call_graph:
            call_graph.nodes[func]["uncovered"] = True

    print("Updated call graph with uncovered functions.")
    return call_graph



def cluster_functions(function_names, num_clusters=5):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(function_names)
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    labels = kmeans.fit_predict(X)
    clusters = {i: [] for i in range(num_clusters)}
    for idx, label in enumerate(labels):
        clusters[label].append(function_names[idx])
    return clusters

def partition_call_graph(call_graph):
    """
    Partition the call graph into connected components of uncovered functions.

    Args:
        call_graph (networkx.DiGraph): The call graph.

    Returns:
        List of sets: Each set contains a group of connected uncovered functions.
    """
    uncovered_groups = []
    uncovered_nodes = {node for node, attr in call_graph.nodes(data=True) if attr.get("uncovered")}

    while uncovered_nodes:
        # Start with one uncovered node
        node = next(iter(uncovered_nodes))

        # Find all connected uncovered nodes
        group = set(nx.node_connected_component(call_graph.to_undirected(), node))
        uncovered_group = group.intersection(uncovered_nodes)

        # Save the group and remove these nodes from further processing
        uncovered_groups.append(uncovered_group)
        uncovered_nodes -= uncovered_group

    return uncovered_groups


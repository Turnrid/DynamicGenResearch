from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import networkx as nx

def cluster_functions(function_names, num_clusters=5):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(function_names)
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    labels = kmeans.fit_predict(X)
    clusters = {i: [] for i in range(num_clusters)}
    for idx, label in enumerate(labels):
        clusters[label].append(function_names[idx])
    return clusters

def partition_call_graph(call_graph, covered_nodes):
    uncovered_groups = []
    for node in call_graph.nodes:
        if node not in covered_nodes:
            group = nx.node_connected_component(call_graph, node)
            uncovered_groups.append(group)
    return uncovered_groups

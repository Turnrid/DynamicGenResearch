from clustering import cluster_functions, partition_call_graph, update_call_graph, CALL_GRAPH_FILE, generate_or_load_call_graph
from functionAnalysis import analyze_groups, save_analysis
from fuzzer_integration import save_test_cases
import networkx as nx

def main():
    # Step 1: Cluster functions (using uncovered functions only)
    uncovered_functions = [
        func for func, attr in call_graph.nodes(data=True) if attr.get("uncovered", False)
    ]
    function_clusters = cluster_functions(uncovered_functions)
    print("Function clusters:", function_clusters)

    # Step 2: Analyze groups with LLM
    analyses = analyze_groups(function_clusters)

    # Step 3: Save analysis and test cases
    save_analysis(analyses)
    save_test_cases(analyses)



if __name__ == "__main__":
    main()

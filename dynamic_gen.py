from clustering import cluster_functions, partition_call_graph, update_call_graph, CALL_GRAPH_FILE, generate_or_load_call_graph
from functionAnalysis import analyze_groups, save_analysis
from fuzzer_integration import save_test_cases
import networkx as nx

def main():
    # Step 1: Generate or load the call graph
    call_graph = generate_or_load_call_graph("function_call_graph.txt")

    # Step 2: Update the call graph with uncovered functions
    call_graph = update_call_graph(call_graph, "uncovered_functions.txt")

    # Step 3: Partition the call graph
    call_graph_groups = partition_call_graph(call_graph)
    print(f"Partitioned uncovered groups: {call_graph_groups}")

    # Step 4: Cluster functions (using uncovered functions only)
    uncovered_functions = [
        func for func, attr in call_graph.nodes(data=True) if attr.get("uncovered", False)
    ]
    function_clusters = cluster_functions(uncovered_functions)
    print("Function clusters:", function_clusters)

    # Step 5: Analyze groups with LLM
    analyses = analyze_groups(function_clusters, call_graph_groups)

    # Step 6: Save analysis and test cases
    save_analysis(analyses)
    save_test_cases(analyses)

    # Step 7: Save the updated call graph
    nx.write_gml(call_graph, CALL_GRAPH_FILE)
    print(f"Updated call graph saved to {CALL_GRAPH_FILE}")

    print("Analysis complete. Results saved in 'function_analysis.txt'.")



if __name__ == "__main__":
    main()

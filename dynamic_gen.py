from clustering import cluster_functions, partition_call_graph
from functionAnalysis import analyze_groups, save_analysis
from fuzzer_integration import save_tests_to_fuzzer, restart_fuzzer

def main():
    # Step 1: Load uncovered functions
    uncovered_functions = []
    with open("uncovered_functions.txt", "r") as f:
        for line in f:
            func_name, func_id = line.strip().split(":")
            uncovered_functions.append(func_name)

    # Step 2: Cluster functions
    function_groups = cluster_functions(uncovered_functions)

    # Step 3: Analyze groups with LLM
    analyses = analyze_groups(function_groups)
    save_analysis(analyses)

    # Step 4: Save tests and restart the fuzzer
    save_tests_to_fuzzer(analyses)
    restart_fuzzer()

if __name__ == "__main__":
    main()

import os
from openai import OpenAI
from collections import defaultdict
from dotenv import load_dotenv

# Load environment variables from the ..env file
load_dotenv()

# Initialize OpenAI client with API key from environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Helper function to load and group functions by common prefix
def load_and_group_functions(filename="uncovered_functions.txt"):
    groups = defaultdict(list)
    functions = []

    with open(filename, 'r') as file:
        for line in file:
            func_name, func_id = line.strip().split(":")
            functions.append(func_name)

    def longest_common_prefix(strs):
        if not strs:
            return ""
        prefix = strs[0]
        for s in strs[1:]:
            while not s.startswith(prefix):
                prefix = prefix[:-1]
                if not prefix:
                    return ""
        return prefix

    while functions:
        func = functions.pop(0)
        common_prefix = longest_common_prefix([func] + functions)

        # Group by common prefix
        matched_functions = [f for f in functions if f.startswith(common_prefix)]
        matched_functions.append(func)
        groups[common_prefix].extend(matched_functions)
        functions = [f for f in functions if not f.startswith(common_prefix)]

    return groups


# Analyze the groups with OpenAI API
def analyze_groups(function_clusters, call_graph_groups):
    """
    Analyze function groups using LLM, incorporating clustering and call graph information.

    Args:
        function_clusters: Dictionary of clusters, where keys are cluster IDs, and values are lists of functions.
        call_graph_groups: List of sets, where each set contains uncovered and connected function names.

    Returns:
        Dictionary mapping group IDs to LLM analyses.
    """
    analyses = {}

    for cluster_id, functions in function_clusters.items():
        # Find which call graph group this cluster intersects with
        related_call_graph_groups = [
            group for group in call_graph_groups if set(functions).intersection(group)
        ]
        
        # Construct a prompt with both clustering and call graph details
        prompt = (
            f"Analyze the following cluster of functions and describe their possible purpose or functionality. "
            "Additionally, consider their connections in the program's call graph:\n\n"
            f"Cluster ID: {cluster_id}\n"
            f"Functions in Cluster:\n" + "\n".join(f"- {func}" for func in functions) + "\n\n"
            f"Call Graph Connections:\n"
            + "\n".join(f"- Connected to: {', '.join(group)}" for group in related_call_graph_groups)
        )
        
        try:
            # Send the combined data to the LLM
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a code analysis assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            analyses[cluster_id] = response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error analyzing cluster {cluster_id}: {e}")
            analyses[cluster_id] = "Analysis failed."
    
    return analyses


# Save the analysis results to a file
def save_analysis(analyses, filename="function_analysis.txt"):
    with open(filename, 'w') as file:
        for group, analysis in analyses.items():
            file.write(f"Group: {group}\n")
            file.write(analysis + "\n\n")

# Main function to execute all steps
def main():
    groups = load_and_group_functions()
    analyses = analyze_groups(groups)
    save_analysis(analyses)
    print("Functionality analysis saved to function_analysis.txt")

if __name__ == "__main__":
    main()

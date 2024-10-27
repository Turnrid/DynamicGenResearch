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
def analyze_groups(groups):
    analyses = {}
    for group, functions in groups.items():
        prompt = (
            f"Analyze the following functions and describe their possible purpose or functionality:\n\n"
            f"Group: {group}\n" + "\n".join(f"- {func}" for func in functions)
        )

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a code analysis assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            analyses[group] = response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error analyzing group {group}: {e}")
            analyses[group] = "Analysis failed."

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

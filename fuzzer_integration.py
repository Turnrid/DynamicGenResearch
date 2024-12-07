import os

def save_test_cases(analyses, output_dir="tests"):
    """
    Save XML test cases based on LLM analyses.

    Args:
        analyses: Dictionary mapping cluster IDs to analysis results.
        output_dir: Directory to save test case files.
    """
    os.makedirs(output_dir, exist_ok=True)

    for cluster_id, analysis in analyses.items():
        test_file = os.path.join(output_dir, f"cluster_{cluster_id}_test.xml")
        with open(test_file, "w") as f:
            f.write(analysis)  # Assuming LLM provides XML-like output or modify accordingly.
    
    print(f"Test cases saved to {output_dir}")



def restart_fuzzer(fuzz_dir="/benchmarks/libxml2/fuzz/in", fuzz_out_dir="/benchmarks/libxml2/fuzz/out", target_binary="/benchmarks/libxml2/fuzz/xmllint_cov"):
    """
    Restart the fuzzer with the given input, output directories, and target binary.
    """
    os.makedirs(fuzz_out_dir, exist_ok=True)
    os.system(f"afl-fuzz -i {fuzz_dir} -o {fuzz_out_dir} -- {target_binary} @@")


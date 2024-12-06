import os

def save_tests_to_fuzzer(test_cases, output_dir="fuzz/in"):
    os.makedirs(output_dir, exist_ok=True)
    for group_id, tests in test_cases.items():
        test_file = os.path.join(output_dir, f"group_{group_id}_tests.txt")
        with open(test_file, "w") as f:
            f.write(tests)

def restart_fuzzer(fuzz_dir="/benchmarks/libxml2/fuzz/in", fuzz_out_dir="/benchmarks/libxml2/fuzz/out", target_binary="/benchmarks/libxml2/fuzz/xmllint_cov"):
    """
    Restart the fuzzer with the given input, output directories, and target binary.
    """
    os.makedirs(fuzz_out_dir, exist_ok=True)
    os.system(f"afl-fuzz -i {fuzz_dir} -o {fuzz_out_dir} -- {target_binary} @@")


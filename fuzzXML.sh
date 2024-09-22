#!/bin/bash

# Set up paths
REPO_PATH="/home/security/DynamicGenResearch"
LIBXML_PATH="$REPO_PATH/benchmarks/libxml2"
FUZZ_INPUT_DIR="$LIBXML_PATH/fuzz/in"
FUZZ_OUTPUT_DIR="$LIBXML_PATH/fuzz/out"

# Create directories for fuzzing
mkdir -p $FUZZ_INPUT_DIR
cp $LIBXML_PATH/libxml2-2.13.0/xmllint $LIBXML_PATH/fuzz/xmllint_cov
cp $LIBXML_PATH/libxml2-2.13.0/test/*.xml $FUZZ_INPUT_DIR

# Configure AFL++ system
cd $LIBXML_PATH/fuzz
afl-system-config

# Run AFL++ fuzzing on libxml2
afl-fuzz -i $FUZZ_INPUT_DIR -o $FUZZ_OUTPUT_DIR -- ./xmllint_cov @@

echo "Fuzzing started, check the output directory for results."

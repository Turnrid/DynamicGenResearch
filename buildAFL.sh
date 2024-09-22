#!/bin/bash

# Set up paths
REPO_PATH="/home/security/DynamicGenResearch"
AFL_PATH="$REPO_PATH/AFLplusplus"
COMMON_PATH="$REPO_PATH/Common"

# Build AFL++
cd $AFL_PATH
make source-only

# Check if AFL++ build was successful
if [ $? -ne 0 ]; then
    echo "AFL++ build failed!"
    exit 1
else
    echo "AFL++ built successfully!"
fi

# Add AFL++ to PATH
export PATH=$PATH:$AFL_PATH

# Build Common libraries
cd $COMMON_PATH
make clean && make

# Check if Common libraries build was successful
if [ $? -ne 0 ]; then
    echo "Common libraries build failed!"
    exit 1
else
    echo "Common libraries built successfully!"
fi

echo "All builds completed successfully!"

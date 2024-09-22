#!/bin/bash

# Set up paths
REPO_PATH="/home/security/DynamicGenResearch"
LIBXML_PATH="$REPO_PATH/benchmarks/libxml2"
LIBXML_VERSION="libxml2-2.13.0"
AFL_COMPILER="afl-cc -fPIC -lshmQueue"
AFL_CPP_COMPILER="afl-c++ -fPIC -lshmQueue"

# Extract libxml2
cd $LIBXML_PATH
tar -xvf $LIBXML_VERSION.tar.xz
cd $LIBXML_VERSION

# Set AFL++ compiler environment variables
export CC=$AFL_COMPILER
export CXX=$AFL_CPP_COMPILER

# Configure and build libxml2 with AFL++
./configure --enable-shared=no
make

# Check if libxml2 build was successful
if [ $? -ne 0 ]; then
    echo "libxml2 build with AFL++ failed!"
    exit 1
else
    echo "libxml2 built with AFL++ successfully!"
fi

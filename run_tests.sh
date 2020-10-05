#! /bin/sh

set -ex

export LEGEND_HOME=/tmp/.legend 

# Run tests

legend configure 
# legend build
echo "Running legend build test"
legend build sample_input.yaml -o sample_output.json -s

# legend apply (also tests the folder creation flow)
echo "Running legend publish test"
legend publish sample_output.json -f SampleFolder 

# TODO: deleting the sampleFolder and sample dashbaord

# TODO: verify input and expected output files

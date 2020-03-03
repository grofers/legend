#! /bin/sh

set -ex

export LEGEND_HOME=/tmp/.legend 

# Run tests

# legend build
echo "Running legend build test"
legend build sample_input.yaml -o sample_output.json -s

# legend apply (also tests the folder creation flow)
echo "Running legend publish test"
legend publish sample_output.json -f SampleFolder 

# deleting the sampleFolder and sample dashbaord
# TODO

# legend publish + if all the metric files and input files are correct (comprehensive test)
echo "Running legend build test and checking all sample inputs and metrics library files"

for f in sample_inputs/*.yaml
    do
        echo "Running legend build for sample_inputs/$f"
        sed '/grafana_folder:/ s/: .*/: test-ci/' $f > transformed.yaml
        legend apply transformed.yaml
        rm transformed.yaml
done

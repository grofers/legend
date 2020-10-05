import os
import subprocess
import time
import yaml
import pytest
from kopf.testing import KopfRunner

handler_py = os.path.relpath(os.path.join(os.path.dirname(__file__), 'handler.py'))
crd_yaml = os.path.relpath(os.path.join(os.path.dirname(__file__), 'crd.yaml'))
input_dir = os.path.join(os.getcwd(),'tests')

# To update the spec of metric_test.yaml
sample_file = os.path.join(os.path.dirname(__file__),'..','sample_input.yaml')
metric_file_crd = os.path.join(input_dir,'metric_test.yaml')

with open(sample_file,'r') as file:
    sample_spec = yaml.load(file, Loader=yaml.FullLoader)

with open(metric_file_crd,'r') as file:
    metric_input = yaml.load(file, Loader=yaml.FullLoader)

metric_input['spec'] = sample_spec

with open(metric_file_crd,'w') as file:
    yaml.dump(metric_input, file, sort_keys=False)


@pytest.fixture(autouse=True)
def test_crd_exists():
    subprocess.run(f"kubectl apply -f {crd_yaml}",
            check=True, timeout=10, capture_output=True, shell=True)


def test_resource_lifecycle():

    # Run an operator and simulate some activity with the operated resource.
    with KopfRunner(['run', '--verbose', '--standalone', handler_py], timeout=60) as runner:

        for file in os.listdir(input_dir):

            input_yaml = os.path.join(input_dir,file)
            subprocess.run(f"kubectl apply -f {input_yaml}",
                        shell=True, check=True, timeout=10, capture_output=True)
            time.sleep(40)  # give it some time to react

            subprocess.run(f"kubectl delete -f {input_yaml}",
                        shell=True, check=True, timeout=10, capture_output=True)
            time.sleep(40)  # give it some time to react

    # Ensure that the operator did not die on start, or during the operation.
    assert runner.exception is None
    assert runner.exit_code == 0
# Legend

Tool to generate grafana dashboard with pre filled metrics 

## Structure 

* The input file should represent a "Service"
* Every service has multiple "Components"
* The component needs to have a matching file in `metrics_library`. The spec is defined <>

Refer to docs in <docs>

## Dependencies

### Install JSONNET
`brew install jsonnet`

### Download the grafonned-lib
`git clone https://github.com/grafana/grafonnet-lib.git`

### Python requirements
`pip3 install -r requirements.txt`
 

## Generate dashboards

### Generate the JSON
`python main.py -f sample_input.yaml`
`jsonnet -J grafonnet-lib output.jsonnet`

### Create Grafana dashboard
Copy paste the output from the above commands into grafana

Create a new dashboard:
----------------------
Grafana > Create > Import > paste JSON

Modify existing dashboard:
-------------------------


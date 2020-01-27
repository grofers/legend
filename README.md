# Legend

<p align="center">
  <img src="http://www.desigifs.com/sites/default/files/2013/BalaKrj2.gif" alt="Legend"/>
</p>

Tool to generate grafana dashboard with pre filled metrics 

### Structure 

* The input file should represent a "Service"
* Every service has multiple "Components"
* The component needs to have a matching file in `metrics_library`. The spec is defined <>

Refer to docs in <docs>

### Dependencies

Install JSONNET 
```
brew install jsonnet
```

Download the grafonned-lib
```
git clone https://github.com/grafana/grafonnet-lib.git
```

Python requirements
```
pip3 install -r requirements.txt
```
 
### Generate dashboards

Generate the JSON
```
python main.py -f sample_input.yaml 
jsonnet -J grafonnet-lib output.jsonnet
```

Copy paste the output from the above commands into grafana
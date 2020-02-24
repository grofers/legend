# Legend

<p align="center">
  <img src="http://www.desigifs.com/sites/default/files/2013/BalaKrj2.gif" alt="Legend"/>
</p>

Tool to generate grafana dashboard with pre filled metrics 

### Directory Structure

* The input file should represent a "Service"
* Every service has multiple "Components"
* The component needs to have a matching file in `metrics_library`. The spec is defined <>

Refer to docs in <docs>

### Install Dependencies

This project is built with python3. Make sure you have python3 installed on your system.

Install Jsonnet with brew
```
brew install jsonnet
```

### Generate Dashboards

Clone this repository to your local
```
git clone git@github.com:grofers/legend.git
```

Create a python3 virtualenv
```
mkvirtualenv -p /usr/local/bin/python3 legend
```

Install requirements from requirements.txt
```
pip3 install -r requirements.txt
```

Set GRAFANA_API_KEY in ENV
```bash
echo 'export GRAFANA_API_KEY="<your_grafana_key>"' >> ~/.bashrc
echo 'export GRAFANA_API_KEY="<your_grafana_key>"' >> ~/.bash_profile
echo 'export GRAFANA_API_KEY="<your_grafana_key>"' >> ~/.zshrc # only if you have zsh
```
 
Run the following command with a dashboard template to generate the dashboard JSON -

```
python main.py -f sample_input.yaml 
```

This output of the above command will be saved to `dashboard.json`. This JSON file can be imported the into Grafana to create your dashboard.

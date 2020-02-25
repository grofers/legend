``# Legend

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
pip install -e .
```

Set GRAFANA_API_KEY in ENV
```bash
echo 'export GRAFANA_API_KEY="<your_grafana_key>"' >> ~/.bashrc
echo 'export GRAFANA_API_KEY="<your_grafana_key>"' >> ~/.bash_profile
echo 'export GRAFANA_API_KEY="<your_grafana_key>"' >> ~/.zshrc # only if you have zsh
```
 
Run the following command with a dashboard template to generate the dashboard JSON -

```
GRAFANA_API_KEY=<your-grafana-key> GRAFANA_HOST=grafana.grofers.com GRAFANA_PROTOCOL=https GRAFONNET_PATH=<path-to-grafonnet> legend -f sample_input.yaml
```

This output of the above command will be saved to `dashboard.json`. This JSON file can be imported the into Grafana to create your dashboard.

### Generate Dashboards via Kubernetes

legend exposes itself as a CRD.

#### Minikube Setup

You can set it up in your minikube for trying out and development:

Start minikube:

```
minikube start
```

Start a proxy to minikube in a terminal and leave it open:

```
kubectl proxy
```

Setup the development environment:

```
mkvirtualenv legend
pip install -e .
pip install -r kubernetes/requirements.txt
```

Setup the CRD and start the operator:

```
cd kubernetes
kubectl apply -f crd.yaml
GRAFANA_API_KEY=<your-grafana-key> GRAFANA_HOST=grafana.grofers.com GRAFANA_PROTOCOL=https GRAFONNET_PATH=<path-to-grafonnet> DEV=true LOG_LEVEL=DEBUG kopf run handler.py
```

Create your dashboard:

```
kubectl apply -f test/obj.yaml
```

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
Legend Home
Legend is dependent upon grafonnet-lib, which is clones in the `LEGEND_HOME`
The default `LEGEND_HOME` is the `~/.legend` for user, you can alter it by setting it as environment variable
If you want to use an other version of grafonnet-lib, you can set that folder to be in the path of `LEGEND_HOME`

Create a python3 virtualenv
```
mkvirtualenv -p /usr/local/bin/python3 legend
```

Install requirements from requirements.txt
```
pip install -e .
```

Set the grafana configurations in `legend.cfg`
```
legend [OPTIONS] COMMAND [ARGS]
```

OR
 
Run the following command with a dashboard template to generate the dashboard JSON -

```
GRAFANA_API_KEY=<your-grafana-key> GRAFANA_HOST=grafana.grofers.com GRAFANA_PROTOCOL=https legend -f sample_input.yaml
```

### To run your tests locally

Export grafana settings to your local environment
```
export GRAFANA_API_KEY=<YOUR_GRAFANA_API_KEY>
export GRAFANA_HOST=grafana-stage.grofers.io
export GRAFANA_PROTOCOL=https
```

Run the test script
```
./tests.sh
```

### Generate Dashboards via Kubernetes

legend exposes itself as a CRD.

#### Deploying via CRD

Set the appropraite context 
`kubectl apply -f <>`

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
GRAFANA_API_KEY=<> GRAFANA_HOST=grafana.grofers.com GRAFANA_PROTOCOL=https LEGEND_HOME=<> DEV=true LOG_LEVEL=DEBUG kopf run handler.py
```

Create your dashboard:

```
kubectl apply -f test/obj.yaml
```

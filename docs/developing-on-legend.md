# Developer's guide

For developing features or fixing bugs on legend, please use this guide 

## Setup

```shell
brew install jsonnet
git clone https://github.com/grofers/legend.git
cd legend
pip install --ignore-installed -e .
```

## Developing on the CLI

### Initial Configuration

Legend needs a basic configuration to work with, you can set the root of the legend home dir
by setting the env variable `LEGEND_HOME`. Legend created a folder `.legend` within the root and
refers config (`legend.cfg`) from that location

Setup the `legend.cfg`

```shell
[grafana]
api_key:
protocol: https
host: grafana-stage.grofer.io
```

## Developing on the CRD

### Deploying via CRD

Set the appropriate context
`kubectl apply -f <>`

### Minikube Setup

You can set it up in your minikube for trying out and development:

Start minikube:

```shell
minikube start
```

Start a proxy to minikube in a terminal and leave it open:

```shell
kubectl proxy
```

Setup the development environment:

```shell
mkvirtualenv legend
pip install --ignore-installed -e .
pip install -r kubernetes/requirements.txt
```

Setup the CRD and start the operator:

```shell
cd kubernetes
kubectl apply -f crd.yaml
GRAFANA_API_KEY=<> GRAFANA_HOST=<> GRAFANA_PROTOCOL=https LEGEND_HOME=<> DEV=true LOG_LEVEL=DEBUG kopf run handler.py
```

Create your dashboard:

```shell
kubectl apply -f test/obj.yaml
```

## Testing

You can test legend by running e2e tests in a completely isolated environment.

Prerequisite
```shell
 * Kind
 * Python 3 (use pyenv or virtualenv)
 * Jsonnet
 * Helm3
 * Docker
```

The following script will spawn a new Kubernetes cluster using kind and will install relevant dependencies on the Kubernetes cluster.
The script will automatically clean the relevant kind cluster. 

```shell
chmod +x isolated_legend_e2e_test.sh
./isolated_legend_e2e_test.sh
```

### Deploying / Publishing

Just raise a PR in the Legend github repo

# Developing on legend

For developing features or fixing bugs on legend, please use this guide 

## Setup

```shell
brew install jsonnet
git clone https://github.com/grofers/legend.git
cd legend
pip install -e .
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

Set the appropraite context 
`kubectl apply -f <>`

### Minikube Setup

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

## Building / testing

Legend does not require a seperae build step, you can validate your changes by running 
the tests. Please note that unlike while running in production, while testing Legend
actually assumes `/tmp/` to be the home root directory. Hence, it is suggested to use this 
in the first place to create a config file `/tmp/.legend/legend.cfg`

Run the tests
```shell
./tests.sh
```

This will verify two things
1. If all the commands of the CLI are working fine (by actually trying to create dashboards)
2. Verifies if there are any breaking changes with the metrics files and input configurations


### Deploying / Publishing

Just raise a PR in the Legend github repo
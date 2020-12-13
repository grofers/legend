#!/bin/bash

## Preequisite
# * Kind
# * Python 3.7 (use pyenv or virtualenv)
# * Jsonnet
# * Helm3
# * Docker

## Run Grafana in detached mode
docker run -d --rm -p 3000:3000 --env-file ./tests_config/env.list -v ./tests_config:/etc/grafana/provisioning --name grafana grafana/grafana:7.1.5

## Create Isolated kind cluster
kind create cluster --name legend-test
kubectl config use-context legend-test

## Install Chart using helm3
helm repo add cloudposse https://charts.cloudposse.com/incubator/
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm dep update
helm3 install --set tag.service-level-operator=true --set tag.kube-prometheus-stack=true --set service-level-operator.enabled=true --set kube-prometheus-stack.enabled=true legend --namespace monitoring .

##Install python dependencies
pip install -r requirements.txt && pip install -r ./kubernetes/requirements.txt && pip install jsonnet && pip install .

## Build legend
python setup.py build

## Run tests
chmod +x run_tests.sh
GRAFANA_HOST=0.0.0.0:3000 GRAFANA_PROTOCOL=http ./run_tests.sh


# Legend

> The legendary tool which builds and manages grafana dashboards for your applications

[![License](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![Release](https://img.shields.io/github/v/tag/grofers/legend)](https://github.com/grofers/legend/releases/tag/v0.1) [![Artifact HUB](https://img.shields.io/endpoint?url=https://artifacthub.io/badge/repository/legend)](https://artifacthub.io/packages/search?repo=legend)

[![Grofers Engineering](https://img.shields.io/badge/Grofers-Engineering-orange)](https://lambda.grofers.com/)

## What is Legend

Legend builds and publishes Grafana dashboards for your services with prefilled metrics and alerts for your services.

Say you got an EC2 to monitor, an S3 to monitor, a Kubernetes cronjob to monitor (or one of many other things); legend has got your back. It will do all the menial work of setting up grafana dashboards for you without you needing to setup grafana dashboards manually or write cloudwatch/prometheus/influxdb queries by hand.

### Methodology

Legend uses the [USE](http://www.brendangregg.com/usemethod.html) and [RED](https://thenewstack.io/monitoring-microservices-red-method/) methodology of monitoring service and infrastructure level metrics.

## Table of contents

* [Features](#features)
* [Getting started](#getting-started)
  * [Pre-requisites](#pre-requisites)
  * [Using Legend](#using-legend)
* [Contribution](#contribution)
* [Legend internals](#legend-internals)

## Features

* Build dashboards for your services with prefilled metrics
* Customizable alerts and panels
* Automatic setup of basic alerts with priority and service mapping
* Beautiful outlay of the dashboard to enable uniformity.
* Currently, here are the following types of components which legend can plot for you:
  * Airflow
  * Amazon ALB
  * Celery
  * Consul
  * CouchDB
  * Django
  * Flask
  * Amazon ELB
  * Go
  * HAProxy
  * JMX
  * Loki
  * MySQL - RDS
  * MySQL - EC2
  * NGINX (Log-based metrics)
  * NodeJS
  * PostgreSQL - RDS
  * PgBouncer
  * Phoenix
  * EC2 Platform level metrics
  * [Kubernetes CronJob](docs/cronjob-prometheus-rule.md)
  * Kubernetes Deployment
  * Kubernetes Horizontal Pod Autoscaler
  * Kubernetes Ingress
  * Playframework
  * Promtail
  * RabbitMQ
  * Redis
  * Redis - Elasticache
  * S3
  * Sprintboot
  * SQS
  * Starlette
  * Hashicorp Vault
* Legend currently has the capability to further have support for any other component, provided that component's log generation is backed by one of the following metric/log stores:
  * Cloudwatch
  * InfluxDB
  * Loki
  * Prometheus

## Getting started

This section describes on how to get started with using Legend.

### Pre-requisites

* For each component of your service, there has to be a respective metric files in
`legend/metrics_library/metrics/` which containes the metrics to be plotted for that component. If you are adding a new component(and a new metric library file) please refer to [contributing-to-metric-library](docs/contributing-to-metric-library.md)

* Based on the component an additional step of enabling metrics for the component has to happen. The monitoring queries written are based on specific exporters userd to expose the metrics, mentioned in [enabling metrics](docs/contributing-to-metric-library.md). If other exporters are used, the queries might have to be changed.

* For cronjobs an additional custom prometheus rule is required. You can find more details [here](docs/cronjob-prometheus-rule.md)
### Using Legend

You can use `legend` in one of the two ways:

* [Use legend in kubernetes](#use-legend-in-kubernetes)
* [Legend CLI](#legend-cli)

**The recommended way to use Legend is to deploy it in Kubernetes**

You need to create an input file describing the components of your service [writing-input-file](docs/writing-input-file.md)

#### Use legend in kubernetes

Legend installs as a CRD in Kubernetes

**Required kubernetes >= 1.16**

*Installation*
Quick instructions
Legend is installed via [helm](https://helm.sh/):

* Add the helm repo: `helm repo add legend https://grofers.github.io/legend`
* Configure Legend, make a local copy of [values.yaml](charts/legend/values.yaml) and edit the values as necessary
* Deploy the chart: `helm install legend legend/legend -f values.yaml`

Legend Helm Chart is hosted [here](https://artifacthub.io/packages/helm/legend/legend)

*Usage*

To use legend via its CRD (Current version: v1beta1), create a spec file in the following format:

```yaml
apiVersion: grofers.io/v1beta1
kind: GrafanaDashboard
metadata:
  name: # Name of the object internally
  labels:
    app: # Add name for reference
spec:
  apiVersion: grofers.io/v1beta1
  kind: GrafanaDashboard
  grafana_dashboard_spec: # The core spec/configuration on the basis of which legend will build the dashboards
    #Dashboard Spec
```

Format for [spec.grafana_dashboard_spec](./sample_input.yaml)

To create/update/delete the dashboard, run:

```shell
kubectl apply -f <input-file.yaml>
kubectl delete -f <input-file.yaml>
```

#### Use Legend CLI

Legend can also be installed as a CLI and used to create dashboards.
> At the current stage, Legend can only create dashboards but not delete them becuase it does not
> record the state of dashboards it created anywhere

*Installation*

Legend requires python3. It is recommended to install legend in a virtual env

```shell
brew install jsonnet
mkvirtualenv -p `which python3` legend
pip install git+https://github.com/grofers/legend
legend configure
```

*Configuration*

`LEGEND_HOME` represents the home directory of Legend, by default it is the home directory of the user.
You can override by setting the `LEGEND_HOME` env variable while running legend

Legend needs a configuration file to talk to Grafana, by default it searches for it in `LEGEND_HOME/.legend/legend.cfg`, you can over-ride this with passing `-c` option while runing the commands.

The format for legend.cfg:
> This is pre-requisite to run legend as a CLI.

```shell
[grafana]
api_key = # Grafana key with write permission if you are using Legend to create a dashboard, if not read permissions to get the alerting id
protocol = [https|http] # ex: https
host = # Grafana host url
```

To configure legend

```shell
legend configure
```

*Running legend*

```shell
Usage: legend [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  apply
  build
  configure
  publish
```

## Contribution

You can contribute to legend in two ways:

*Developing/improving legend's functionality*

* You can pick up the existing issues in the github repo of legend and work on the fixes.
* Or, you can raise an issue (bug-report or feature-request).
* Fork this repo and setup up a branch on your forked repo to work on the contribution.
* Follow the guide [developing on legend](docs/developing-on-legend.md) for getting a detailed idea about the rightful way of developing and testing over legend.
* Raise the PR containing the reference to the issue it intends to solve.

*Improve the metrics legend creates for a service*
* This is one of the biggest offerings of Legend - pre configured metrics for a wide variety of
components.
* If you are contibuting to the existing metrics or writing new ones please follow the giude [contributing-to-metric-library](docs/contributing-to-metric-library.md)
* To Run e2e tests locally follow the guide [testing on legend](docs/developing-on-legend.md#testing).

* Raise a PR

## Legend internals

[Legend internals](docs/legend-internals.md)

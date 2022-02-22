# Monitoring and alerting Kubernetes cronjobs

> The default metrics available in Kubernetes are not sufficient to monitor and set alerts on cronjobs. We will add a custom metric to achieve this.

## Overview

Legend uses custom Prometheus rule to set alerting and monitoring on Kubernetes cronjobs. We have followed [this document](https://medium.com/@tristan_96324/prometheus-k8s-cronjob-alerts-94bee7b90511) by `Tristan Colgate-McFarlane`. The document explains the need to add custom metrics and how it is done. We have made some minor changes in the metric query to make it work for the latest kube-state-metrics.

## Metrics library

All the metrics plotted per component are part of the metrics library which lives within legend at `legend/metrics_library/metrics`.
Each component has an associated metrics file in the metrics library in the format
`<component>_metrics.yaml`. The metrics file is a Jinja2 template that is rendered to
a yaml file.

## Use

You can apply the below Kubernetes manifest on your cluster to add custom metrics. You must have this CRD - `monitoring.coreos.com/v1` available on your cluster to apply this rule.

To use this yaml copy and paste this in a file. Then use kubectl to apply in the cluster.

`kubectl apply -f <file-name.yaml> -n <namespace>`

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: cronjob-prometheus-metric
  labels:
    app: kube-prometheus-stack
    release: prom-op
spec:
  groups:
  - name: ./cronjob.rules
    rules:
    - record: job:kube_job_status_start_time:max
      expr: |
        label_replace(
          label_replace(
            max(
              kube_job_status_start_time
              * ON(job_name,namespace) GROUP_RIGHT()
              kube_job_owner{owner_name!=""}
            )
            BY (job_name, owner_name, namespace)
            == ON(owner_name) GROUP_LEFT()
            max(
              kube_job_status_start_time
              * ON(job_name,namespace) GROUP_RIGHT()
              kube_job_owner{owner_name!=""}
            )
            BY (owner_name),
          "job", "$1", "job_name", "(.+)"),
        "cronjob", "$1", "owner_name", "(.+)")
    - record: job:kube_job_status_failed:sum
      expr: |
        clamp_max(
          job:kube_job_status_start_time:max,1)
          * ON(job,namespace) GROUP_LEFT()
          label_replace(
            label_replace(
              (kube_job_status_failed != 0),
              "job", "$1", "job_name", "(.+)"),
            "cronjob", "$1", "owner_name", "(.+)")
```

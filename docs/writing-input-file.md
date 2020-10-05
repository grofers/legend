# Writing input file for legend

For legend, every input file  correlates to _one_ Grafana dashboard. Every dashboard represts one
[service](#service) which is built up of multiple [components](#components).

The input file must be written in [yaml](#yaml) format

## Service

The construct of service is similar to the application for which the dashboard is being built for

## Components

These are discrete components which the application is using to provide the service. Simply put - this can be all the tech stack of the application's architecture

## Metric library

A core feature of Legend is that it creates dashboards with pre filled metrics. All these metrics are stored in [metric library](../legend/metrics_library/metrics). Every file in this folder represents the default metrics which are plotted for that component. The default alerting configuration is also defined in the same file.

The metrics here have been coallated using standard industry practices, you can find some of the
references here:

* https://landing.google.com/sre/sre-book/chapters/monitoring-distributed-systems/
* https://www.vividcortex.com/blog/monitoring-and-observability-with-use-and-red
* https://grafana.com/files/grafanacon_eu_2018/Tom_Wilkie_GrafanaCon_EU_2018.pdf
* https://www.slideshare.net/OpsStack/how-to-monitoring-the-sre-golden-signals-ebook/
* https://medium.com/@copyconstruct/monitoring-in-the-time-of-cloud-native-c87c7a5bfa3e

The file [sample_input.yaml](../sample-input.yaml) has all the components supported by legend.
If there are no metrics for the components your service is using, please consider contributing to the
metric library, [contributing-to-metric-library](../docs/contributing-to-metric-library.md)

## Sample input

All descriptional fields of this spec are compulsory. For fileds within components you can refer to the [schema](../legend/metrics_library/metrics_schema.py) to find out which ones are compulsory and optional

```yaml
---
title: # Title of the dashboard. Should ususally be the service name. While creating the title in Grafana, this is appended with the environment filed mentioned below
service: # Name of the service for which the dashboard is being generated. For all the alerts in this dashboard, a tag og_servce:<service> will be created which is further used for associating alerts from this dashabord to a particular service in opsgenie 
grafana_folder: # The grafana folder in which the dashboard has to be created. If the folder is not present in Grafana, Legend creates it
alert_channels: [] # List of alert channels for notifications. These have to be present in Grafana from before
environment: # The environment for which the dashboard is being generated for
description: # Description on what is the pupose of the service/application
references:
  deployment: # Reference link to tell how the service is deployed
  documentation: # Reference link to the service's documentation
  metrics_definition: # Reference link to the service's metrics definition
tags: # List of tags for the grafana dashboard
components: # The components which the service consists of along with the identifiers
  s3: # Components name
    dimensions: # unique identifiers for the component. The unique identifiers for the component can be seen in the sample input file or in the schema. 
        - bucket_name: #
        filter_id: EntireBucket
```

## Add custom metrics and alert configurations

To suit your use case you can edit the default alerts and metrics for each component. Or create new
panels with custom metrics. You need to add the sepc in the input file under the component for which the config has to be changed. If the panel title is new a new panel is created, if not the existing panel will be alerted.

The custom panels/metrics should follow the same format/syntax from the original component file in `metrics_library/metrics`. Please refer to [contributing-to-metric-library](../docs/contributing-to-metric-library.md) to understand this spec

```yaml
  sqs:
    dimensions:
      - queue_name: pos_upstream_data_log
        dead_queue_name: pos_upstream_data_log_dead
    panels: # Custom panel spec
      - title: (E) Dead Queue depth(Total messages)
        alert_config:
          priority: P3
          message: 'dead queue depth is higher than 10'
          rule:
            for_duration: 5m
            evaluate_every: 1m
          condition_query:
            - OR,avg,1,now,5m,gt,10
```

```yaml
alert_config: # Alert spec
    priority: P2
    message: '(U) Database Connection Utilization (%) is HIGH'
    rule:
      for_duration: 5m
      evaluate_every: 10s
    condition_query:
    - OR,avg,1,now,5m,gt,20
    - OR,avg,2,now,5m,gt,30
```

# Contributing to metric library
> The default metrics which are plotted for every component within a service

## Metrics library 

All the metrics plotted per component are part of the metrics library which lives within legend. 
Each component has an associated metrics file in the metrics library in the format 
`<component>_metrics.yaml`. The metrics file is actually a jinja2 template which is rendered to 
be a yaml file. 

## Spec

The input file has to be written based on the data source of the metrics. 
Each component is seperate with a `row` panel in grafana, and the panels within each of these
consists of one or more `targets`. These are the actual graphs which are plotted in Grafana. 

Legend uses [grafonnet-lib](https://github.com/grafana/grafonnet-lib/tree/v0.1.0) internally to generat the
dashboard's json and apply it to Grafana. 

### Basic spec
```yaml
component: # Components name
data_source: # Datasource of the metrics
metrics_source: # How are the metrics being exposed by the component - default(framework is exposing by itslef/have to be enabled on the managed service) | <exporter name>
reference: # Reference link to the components documentation
description: # Short description on what the component does
```

### Panels
```yaml
panels: # The metrics to be plotted
- title: # Title of the panel
    type: # Type of the panel in Grafana. Currently only 'graph' is supported in legend
    description: # Describe what the panel represents
    targets:
    {% for dimension in data %} # The 'dimensions' dict from the input file is passed to the targets
      - metric: django_http_responses_total_by_status_total{job=~"{{ dimension.job }}"} # metric to be plotted. You can use jinja2 templating fill in the vars passed in the input file
        legend: # Legend to be displayed in the panel. Optional.
        ref_no: 1 # Reference number which is used in the alert config. Do not confuse with the ref_id which Grafana creates. 'ref_no' is internal, but when the grafana dashboard is created grafana actually creates a ref id (from A to Z). Legend associates the ref_no to the ref_id and sets the appropriate alert rule on the metric
      - metric: # second metric
        legend: '{{ '{{instance}}' }}'
        ref_no: 2 # Incremenatal ref_no, used to associate alerts to this particular metric
    {% endfor %}
    alert_config: # Alert config
      priority: # Priority of the alert. Must be one of P1-P5. This is configured as a tag in grafana with the key:value - og_priority:<priority>. This priority is associated to the alert/incident in opsgenie automatically
      message: # Alerting message
      rule: # Alerting rule, follows the alerting rules from Grafana
        for_duration: 5m # Sample
        evaluate_every: 10s # Sample
      condition_query: # The list of condition queries, evaluated per target. Follows the same format as described in Grafana alerts
      - OR,avg,1,now,5m,gt,20 # The first condition is automatically converted to 'WHEN' when the alert if being configured in grafana. The ref_no of the target must be filled in the third field to reference which target has to be evaluated against this rule. 
      - OR,avg,2,now,5m,gt,30

```

### Addtional Spec
``` yaml
formatY1: # The fomat of the data in the Y1 axis, this follows the Grafana standard (sample : Bps, bytes, s, percent)
labelY1:  # The label to put in the Y1 graph panel (sample : bytes/sec , bytes , seconds, percent)
```

## Adding metrics for new components

* If you are addining metrics for a new component, please follow the spec as mentioned above. 
* The variables and the component spec has to be added in the [metrics_schema](../legend/metrics_library/metrics_schema.py) and import the configuration into the [schema](../legend/metrics_library/schema.py) to ensure proper validation - this will enable input validation.
* In the [sample_input.yaml](../sample_input.yaml) add the component with basic/sample confiugration - this will enable testing and ensure backward compatability also making adaptability easy
* Reference in  confluence - [here](https://grofers.atlassian.net/wiki/spaces/IN/pages/1491140622/Exposing+metrics+on+services),  on how to enale the metrics along with the exporters which it is using (where required)
* Please refer to proper documentation the component for creating appropriate metrics
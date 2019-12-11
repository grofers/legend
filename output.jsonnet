
local grafana = import 'grafonnet/grafana.libsonnet';
local dashboard = grafana.dashboard;
local template = grafana.template;
local text = grafana.text; 
local row = grafana.row;
local singlestat = grafana.singlestat;
local graphPanel = grafana.graphPanel;
local prometheus = grafana.prometheus;
local cloudwatch = grafana.cloudwatch;
local influxdb = grafana.influxdb;

local S3 = 
    row.new(title='S3')
    ; 
local SThrottles = 
    graphPanel.new(
        title='(S) Throttles',
        datasource='$CLOUDWATCH_DS',
        legend_values='true',
        legend_min='true',
        legend_max='true',
        legend_current='true',
        legend_total='false',
        legend_avg='true',
        legend_alignAsTable='true',
    )

.addTarget(
    cloudwatch.target(
    'default',
    'AWS/DynamoDB',
    'ReadThrottleEvents',
    datasource=null,
    statistic='Sum',
    alias=null,
    highResolution='false',
    period='1m',
    dimensions={'BucketName': 'grofers-loki-stage', 'FilterId': 'EntireBucket'}
    )
)

.addTarget(
    cloudwatch.target(
    'default',
    'AWS/DynamoDB',
    'WriteThrottleEvents',
    datasource=null,
    statistic='Sum',
    alias=null,
    highResolution='false',
    period='1m',
    dimensions={'BucketName': 'grofers-loki-stage', 'FilterId': 'EntireBucket'}
    )
)
; 
local Promtail = 
    row.new(title='Promtail')
    ; 
local EMissingpods = 
    graphPanel.new(
        title='(E) Missing pods',
        datasource='$PROMETHEUS_DS',
        legend_values='true',
        legend_min='true',
        legend_max='true',
        legend_current='true',
        legend_total='false',
        legend_avg='true',
        legend_alignAsTable='true',
    )

.addTarget(
    prometheus.target(
    '(count(kube_node_info) - count(kube_pod_info{pod=~".*.*"}))',
    )
)

.addTarget(
    prometheus.target(
    '(count(kube_node_info) - count(kube_pod_info{pod=~".*.*"}))',
    )
)
; 
local SystemCoreec2 = 
    row.new(title='SystemCore-ec2')
    ; 
local UMemoryutilisation = 
    graphPanel.new(
        title='(U) Memory utilisation',
        datasource='$INFLUXDB_DS',
        legend_values='true',
        legend_min='true',
        legend_max='true',
        legend_current='true',
        legend_total='false',
        legend_avg='true',
        legend_alignAsTable='true',
    )

.addTarget(
    influxdb.target(
    "SELECT mean('value') FROM 'memory_value' WHERE ('type_instance' = 'used' AND 'host' =~ /^bind/ AND 'type' = 'percent') AND $timeFilter GROUP BY time($interval), 'host' fill(null)",
    '$tag_host',
    )
)
; 
local sdp = 
    text.new(
        title='Service Description',
        span=null,
        mode='markdown',
        content='# LokiFromCode \n \n  #### Components  \n \n  [S3](https://aws.amazon.com/s3/): Provide a reliable solution for object level storage  \n \n[Promtail](https://github.com/grafana/loki/tree/master/docs/clients/promtail): Scrapes logs from pods and pushes them to loki, deployed as daemonset across all nodes  \n \n[SystemCore-ec2](https://www.slideshare.net/OpsStack/how-to-monitoring-the-sre-golden-signals-ebook/): System core metrics  \n \n \n \n #### References \n \n [Deployment](https://github.com/grofers/kube-infra/tree/master/manifests/loki) \n \n[Documentation](https://github.com/grafana/loki/tree/master/docs) \n \n[Metrics definition](https://github.com/grofers/kube-infra/tree/master/manifests/loki) \n \n',
        transparent=null,
        description=null,
        datasource=null,
    )
; 

dashboard.new(
'LokiFromCode',
tags=['stage', 'infra'],
schemaVersion=18,
editable='true',
time_from='now-1h',
refresh='1m',
)
.addTemplate(
template.datasource(
    'PROMETHEUS_DS',
    'prometheus', 
    'Prometheus (Stage)',
    hide='variable',
    label=null,
    regex="/^Prometheus.*Stage/i"
    )
)
.addTemplate(
template.datasource(
    'CLOUDWATCH_DS',
    'cloudwatch', 
    'Cloudwatch (Stage)',
    hide='variable',
    label=null,
    regex="/.Stage/i"
    )
)
.addTemplate(
template.datasource(
    'INFLUXDB_DS',
    'influxDB', 
    'InfluxDB (Stage)',
    hide='variable',
    label=null,
    regex="/^InfluxDB .Stage/i"
    )
)

.addPanels([ sdp  { gridPos: { h: 10, w: 15, x: 0, y: 0 }, }, ])

    .addPanels(
  [
    S3  { gridPos: { h: 4, w: 24, x: 0, y: 1 }, }, 
SThrottles  { gridPos: { h: 8, w: 12, x: 0, y: 2 }, }, 
Promtail  { gridPos: { h: 4, w: 24, x: 0, y: 3 }, }, 
EMissingpods  { gridPos: { h: 8, w: 12, x: 0, y: 4 }, }, 
SystemCoreec2  { gridPos: { h: 4, w: 24, x: 0, y: 5 }, }, 
UMemoryutilisation  { gridPos: { h: 8, w: 12, x: 0, y: 6 }, }, 

  ]
)


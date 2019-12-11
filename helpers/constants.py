#!/usr/bin/env python

############
#
#Dashboards
#
############

#Dashboard

IMPORTS = """
local grafana = import 'grafonnet/grafana.libsonnet';
local dashboard = grafana.dashboard;
local template = grafana.template;
local row = grafana.row;
local singlestat = grafana.singlestat;
local graphPanel = grafana.graphPanel;
local prometheus = grafana.prometheus;
local cloudwatch = grafana.cloudwatch;
local influxdb = grafana.influxdb;
"""

DASHBOARD_HEAD = '''
dashboard.new(
'{title}',
description="{desc}",
tags={tags},
schemaVersion=18,
editable='true',
time_from='now-1h',
refresh='1m',
)
.addTemplate(
template.datasource(
    'PROMETHEUS_DS',
    'prometheus', 
    'Prometheus ({Env})',
    hide='variable',
    label=null,
    regex="/^Prometheus.*{Env}/i"
    )
)
.addTemplate(
template.datasource(
    'CLOUDWATCH_DS',
    'cloudwatch', 
    'Cloudwatch ({Env})',
    hide='variable',
    label=null,
    regex="/.{Env}/i"
    )
)
.addTemplate(
template.datasource(
    'INFLUXDB_DS',
    'influxDB', 
    'InfluxDB ({Env})',
    hide='variable',
    label=null,
    regex="/^InfluxDB .{Env}/i"
    )
)
'''

#Templates


############
#
#Panels
#
############

#Graph
GRAPH_PANEL = '''
    graphPanel.new(
        title='{title}',
        datasource='{datasource}',
        legend_values='true',
        legend_min='true',
        legend_max='true',
        legend_current='true',
        legend_total='false',
        legend_avg='true',
        legend_alignAsTable='true',
    )
'''
#SingleStat


############
#
#Targets
#
############


#cloudwatch
CLOUDWATCH_TARGET = '''
.addTarget(
    cloudwatch.target(
    'default',
    '{namespace}',
    '{metric}',
    datasource=null,
    statistic='{statistic}',
    alias=null,
    highResolution='false',
    period='1m',
    dimensions={dimensions}
    )
)
'''


#prometheus
PROMETHEUS_TARGET = '''
.addTarget(
    prometheus.target(
    '{metric}',
    )
)
'''

#influx
INFLUX_TARGET = '''
.addTarget(
    influxdb.target(
    "{query}",
    '{alias_by}',
    )
)
'''
#!/usr/bin/env python

############
#
# Constants
#
############

# Grafana DB
# Grafana API readonly key, hence plain text
GRAFANA_API_KEY = "***REMOVED***"
GRAFANA_URL = "https://grafana.grofers.com/api"

# Service description components
SERVICE_DESC_INDIVIDUAL_COMPONENT = '[{component}]({component_ref}): {component_desc}'

SERVICE_DESC = '# {{ service }} {% raw %}\\<placeHolder>n  {% endraw %} #### Components {% raw %} \\<placeHolder>n  {% endraw %} {% for item in SERVICE_DESC_INDIVIDUAL_COMPONENTS -%} {{ item }} {% raw %}  \\<placeHolder>n{% endraw %}{% endfor -%}{% raw %} \\<placeHolder>n \\<placeHolder>n {% endraw %}#### References{% raw %} \\<placeHolder>n  {% endraw %}{% for dict_item in references -%} {% for k,v in dict_item.items() -%} [{{ k }}]({{ v }}){% raw %} \\<placeHolder>n {% endraw %}{% endfor -%}{% endfor -%}'

############
#
# Dashboards
#
############

# Dashboard

IMPORTS = """
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
local alertCondition = grafana.alertCondition;
"""

DASHBOARD_HEAD = '''
dashboard.new(
'{title}',
tags={tags},
schemaVersion=18,
editable='true',
time_from='now-1h',
refresh='1m',
)
'''

# Templates


############
#
# Panels
#
############

# Graph
GRAPH_PANEL = '''
    graphPanel.new(
        title='{title}',
        datasource='{datasource}',
        shared_tooltip='true',
        legend_values='true',
        legend_min='true',
        legend_max='true',
        legend_current='true',
        legend_total='false',
        legend_avg='true',
        legend_alignAsTable='true',
        nullPointMode='connected',
    )
'''

# Text
TEXT_PANEL = '''
    text.new(
        title='{title}',
        span=null,
        mode='markdown',
        content='{content}',
        transparent=null,
        description=null,
        datasource=null,
    )
'''

# SingleStat


############
#
# Targets
#
############


# cloudwatch
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

# prometheus
PROMETHEUS_TARGET = '''
.addTarget(
    prometheus.target(
    '{metric}',
    )
)
'''

# influx
INFLUXDB_TARGET = '''
.addTarget(
    influxdb.target(
    "{query}",
    '{alias_by}',
    )
)
'''


############
#
# Alerts and monitoring
#
############

ADD_ALERT = '''
.addAlert(
      '{rule_name}',
      executionErrorState='alerting',
      forDuration='{forDuration}',
      frequency='{evaluate_every}',
      handler=1,
      message='Severity: {severity}',
      noDataState='no_data',
      notifications={AlertChannels},
    )
'''
ADD_ALERT_CONDITION = '''
.addCondition(
    alertCondition.new(
        evaluatorParams=[{evaluatorParams}],
        evaluatorType='{evaluatorType}',
        operatorType='{operatorType}',
        queryRefId='{queryRefId}',
        queryTimeEnd='{queryTimeEnd}',
        queryTimeStart='{queryTimeStart}',
        reducerParams={reducerParams},
        reducerType='{reducerType}',
    )
)
'''

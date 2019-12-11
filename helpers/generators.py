#!/usr/bin/env python

import helpers.constants
from jinja2 import Template, Environment, FileSystemLoader
import yaml

def DASHBOARD_HEAD(title,tags,desc,env):
    head = helpers.constants.DASHBOARD_HEAD.format(title=title,desc=desc,tags=str(tags),Env=env)
    return (head)

def ADD_GRAPH(data_source,panel_data):
    if data_source == "cloudwatch" :
        panel = helpers.constants.GRAPH_PANEL.format(title=panel_data["Title"],datasource='$CLOUDWATCH_DS')
        for target in panel_data["Targets"]:
            target = helpers.constants.CLOUDWATCH_TARGET.format(namespace=target["namespace"],metric=target["metric"],statistic=target["statistic"],dimensions=target["dimensions"])
            panel = panel+target
        return (panel)

    elif data_source == "prometheus":
        panel = helpers.constants.GRAPH_PANEL.format(title=panel_data["Title"],datasource='$PROMETHEUS_DS')
        for target in panel_data["Targets"]:
            target = helpers.constants.PROMETHEUS_TARGET.format(metric=target["metric"])
            panel = panel+target
        return (panel)

    elif data_source == "influxdb":
        panel = helpers.constants.GRAPH_PANEL.format(title=panel_data["Title"],datasource='$INFLUXDB_DS')
        for target in panel_data["Targets"]:
            target = helpers.constants.INFLUX_TARGET.format(query=target["query"],alias_by=target["alias_by"])
            panel = panel+target
        return (panel)

    else:
        raise Exception ("Unsupported data source: %s" % data_source)
    return (panel)

def ADD_SINGLESTAT(data_source,data):
    return()

def ADD_PANEL(data_source,panel_data):
    panel_type = panel_data["Type"]

    if panel_type == "Graph":
        panel = ADD_GRAPH(data_source,panel_data)
    elif panel_type == "SingleStat":
        panel = ADD_SINGLESTAT(data_source,panel_data)
    else:
        raise Exception("Unsupported panel type: %s" % panel_type)
    return (panel)

def ADD_ROW(component):
    row = '''
    row.new(title='{title}')
    '''
    row = row.format(title=component)
    return (row)
    
def ADD_COMPONENT(component,InputIdentifierKeys):
    panels_constants = {}
    panels_list = {}
    
    #Render the jinja2 template
    file_loader = FileSystemLoader('metrics_library') 
    env = Environment(loader=file_loader)
    template = env.get_template(component.lower() + "_metrics.yaml")
    template = template.render(IdentifierKeys=InputIdentifierKeys)
    
    #Load yaml into json
    component_metrics = yaml.load(template)
    data_source = component_metrics["Datasource"]

    #Removing special chars and spaces to avoid JSONNET errors
    componentIdentification = ''.join(e for e in component if e.isalnum())

    #Generate panel constants
    panels_constants[componentIdentification] = ADD_ROW(component)

    #Generate panels along with metrics
    panels_list[componentIdentification] = []

    for panel in component_metrics["Panels"]:
        panelIdentification = ''.join(e for e in panel["Title"] if e.isalnum())
        panels_constants[panelIdentification] = ADD_PANEL(data_source,panel)
        panels_list[componentIdentification].append(panelIdentification)
    return (panels_constants,panels_list)
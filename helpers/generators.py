#!/usr/bin/env python

import yaml
import requests
from jinja2 import Template, Environment, FileSystemLoader
import helpers.constants


def get_alert_id(AlertChannels):
    grafana_notification_channel_uid = []
    grafana_api_key = helpers.constants.GRAFANA_API_KEY
    grafana_url = helpers.constants.GRAFANA_URL
    api_url = grafana_url + "/alert-notifications/lookup"
    headers = {'Authorization': 'Bearer ' + grafana_api_key,
               'Content-Type': 'application/json',
               'Accept': 'application/json'}
    r = requests.get(api_url, headers=headers)
    for g_data in r.json():
        if g_data["name"] in AlertChannels:
            grafana_notification_channel_uid.append({"uid": g_data["uid"]})

    return(grafana_notification_channel_uid)


def add_alert(panel_data, ServiceEnvironment, AlertChannels):
    if "AlertsConfig" in panel_data:
        alertConf = panel_data["AlertsConfig"][ServiceEnvironment]
        grafana_notification_channel_uid = get_alert_id(AlertChannels)
        alert = helpers.constants.ADD_ALERT.format(
            evaluate_every=alertConf["Rule"]["evaluate_every"],
            forDuration=alertConf["Rule"]["forDuration"],
            severity=alertConf["Severity"],
            AlertChannels=grafana_notification_channel_uid,
            rule_name=panel_data["Title"])

        for condition in alertConf["Conditions"]:
            alert += helpers.constants.ADD_ALERT_CONDITION.format(
                evaluatorParams=condition["evaluatorParams"],
                evaluatorType=condition["evaluatorType"],
                operatorType=condition["operatorType"],
                queryRefId=condition["queryRefId"],
                queryTimeEnd=condition["queryTimeEnd"],
                queryTimeStart=condition["queryTimeStart"],
                reducerParams=condition["reducerParams"],
                reducerType=condition["reducerType"])
        return(alert)
    else:
        return ("")


def add_graph(data_source, panel_data, ServiceEnvironment):
    if data_source == "Cloudwatch":
        ds = 'Cloudwatch ({Env})'.format(Env=ServiceEnvironment)
        panel = helpers.constants.GRAPH_PANEL.format(
            title=panel_data["Title"], datasource=ds)
        for target in panel_data["Targets"]:
            target = helpers.constants.CLOUDWATCH_TARGET.format(
                namespace=target["namespace"],
                metric=target["metric"],
                statistic=target["statistic"],
                dimensions=target["dimensions"],
                alias=target.get("alias", "null"),
            )
            panel = panel+target
        return (panel)

    elif data_source == "prometheus":
        ds = 'Prometheus ({Env})'.format(Env=ServiceEnvironment)
        panel = helpers.constants.GRAPH_PANEL.format(
            title=panel_data["Title"],
            datasource=ds)
        for target in panel_data["Targets"]:
            target = helpers.constants.PROMETHEUS_TARGET.format(
                metric=target["metric"])
            panel = panel+target
        return (panel)

    elif data_source == "influxdb":
        ds = 'InfluxDB ({Env})'.format(Env=ServiceEnvironment)
        panel = helpers.constants.GRAPH_PANEL.format(
            title=panel_data["Title"],
            datasource=ds)
        for target in panel_data["Targets"]:
            # Converting " to ' to avoid misconfig
            target["query"] = target["query"].replace("\"", "\'")
            target = helpers.constants.INFLUXDB_TARGET.format(
                query=target["query"],
                alias_by=target["alias_by"])
            panel = panel+target
        return (panel)

    else:
        raise Exception("Unsupported data source: %s" % data_source)
    return (panel)


def add_singlestat(data_source, data, ServiceEnvironment):
    return()


def add_panel(data_source, panel_data, ServiceEnvironment, AlertChannels):
    panel_type = panel_data["Type"]

    if panel_type == "Graph":
        panel = add_graph(data_source, panel_data, ServiceEnvironment)
        # Add Alerts
        alerts = add_alert(panel_data, ServiceEnvironment, AlertChannels)
        panel = panel + alerts
    elif panel_type == "SingleStat":
        panel = add_singlestat(data_source, panel_data, ServiceEnvironment)
    else:
        raise Exception("Unsupported panel type: %s" % panel_type)
    return (panel)


def add_row(component):
    row = '''
    row.new(title='{title}')
    '''
    row = row.format(title=component)
    return (row)


def add_component(component, InputIdentifierKeys, ServiceEnvironment,
                  AlertChannels):
    panels_constants = {}
    panels_list = {}

    # Render the jinja2 template
    file_loader = FileSystemLoader('metrics_library')
    env = Environment(loader=file_loader)
    template = env.get_template(component.lower() + "_metrics.yaml")
    template = template.render(IdentifierKeys=InputIdentifierKeys)

    # Load yaml into json
    component_metrics = yaml.load(template)
    data_source = component_metrics["Datasource"]

    # Removing special chars and spaces to avoid JSONNET errors
    componentIdentification = ''.join(e for e in component if e.isalnum())

    # Generate panel constants
    panels_constants[componentIdentification] = add_row(component)

    # Generate panels along with metrics
    panels_list[componentIdentification] = []

    # Generate component ref for decs text box in dashbaord
    component_ref = helpers.constants.SERVICE_DESC_INDIVIDUAL_COMPONENT.format(
        component_desc=component_metrics["Description"],
        component_ref=component_metrics["Reference"],
        component=component)
    for panel_data in component_metrics["Panels"]:
        panelIdentification = ''.join(
            e for e in panel_data["Title"] if e.isalnum())
        panels_constants[panelIdentification] = add_panel(
            data_source, panel_data, ServiceEnvironment, AlertChannels)
        panels_list[componentIdentification].append(panelIdentification)
    return (panels_constants, panels_list, component_ref)

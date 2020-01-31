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

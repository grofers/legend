import yaml
from jinja2 import Environment, FileSystemLoader
import helpers.constants
import requests


def input_yaml_to_json(input_file):
    with open(input_file, 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exc:
            raise Exception(exc)


def str_yaml_to_json(str):
    try:
        return yaml.load(str)
    except yaml.YAMLError as exc:
        raise Exception(exc)


def jinja2_to_render(directory, filename, data):
    file_loader = FileSystemLoader(directory)
    env = Environment(loader=file_loader)
    template = env.get_template(filename)
    return template.render(data=data)


def assemble_panels(panels_dict):

    assembled_panels = ''

    n = 1
    for k, v in panels_dict.items():
        assembled_panels += k + \
                           "  { gridPos: { h: 4, w: 24, x: 0, y: " + str(n) + " }, }, \n"
        n += 1
        for i in range(0, len(v), 2):
            try:
                assembled_panels += str(v[i]) \
                                   + " { gridPos: { h: 8, w: 12, x: 0, y: " \
                                   + str(n) + " }, }, \n" \
                                   + v[i + 1] \
                                   + " { gridPos: { h: 8, w: 12, x: 12, y: " \
                                   + str(n) + " }, }, \n"
            except IndexError as e:
                assembled_panels += v[i] + \
                                   "  { gridPos: { h: 8, w: 12, x: 0, y: " + \
                                   str(n) + " }, }, \n"
            n += 1

    return assembled_panels

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

    return (grafana_notification_channel_uid)

def parse_condition_query(condition_queries):
    conditions = []
    for condition_query in condition_queries:
        parts = condition_query.split(',')
        if len(parts) != 7:
            raise Exception('Condition query parameters not complete')
    
        conditions.append({'operatorType': parts[0],
                'reducerType': parts[1], 
                'queryRefId': parts[2],
                'queryTimeEnd': parts[3],
                'queryTimeStart': parts[4],
                'evaluatorType': parts[5],
                'evaluatorParams': parts[6],
                'reducerParams': [],
                })
    return conditions
    
    
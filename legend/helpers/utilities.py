import requests
import json
import yaml
import os
import re
from jinja2 import Environment, FileSystemLoader


def convert_to_alnum(st):
    return re.sub(r'\W+', '', st)


def input_yaml_to_json(input_file):
    with open(input_file, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            raise Exception(exc)


def str_yaml_to_json(st):
    try:
        return list(yaml.safe_load_all(st))
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
                           " { gridPos: { h: 4, w: 24, x: 0, y: " + str(n) + " }, }, \n"
        n += 1
        for i in range(0, len(v), 2):
            try:
                assembled_panels += str(v[i]) \
                                   + " { gridPos: { h: 8, w: 12, x: 0, y: " \
                                   + str(n) + " }, }, \n" \
                                   + v[i + 1] \
                                   + " { gridPos: { h: 8, w: 12, x: 12, y: " \
                                   + str(n) + " }, }, \n"
            except IndexError:
                assembled_panels += v[i] + \
                                   "  { gridPos: { h: 8, w: 12, x: 0, y: " + \
                                   str(n) + " }, }, \n"
            n += 1

    return assembled_panels


def assemble_panels_dynamic(input_dashboard):

    assembled_panels = ''

    ri = 0
    r = 0
    for _, v in input_dashboard.get('components').items():
        ri += 1
        r += 1
        assembled_panels += "R_" + str(ri) \
                            + " { gridPos: { h: 4, w: 24, x: 0, y: " + str(r) + " }, }, \n"

        for metric_idx in range(len(v['metric'])):  
            metric = v['metric'][metric_idx]
            panels_in_row = metric.get('panels_in_row', 2)
            if panels_in_row < 1:
                panels_in_row = 2
            elif panels_in_row > 8:
                panels_in_row = 8

            pi = 0
            while True:
                r += 1
                p = 0
                row_end = min(len(metric.get('panels')), pi + panels_in_row)
                width = int(24 / (row_end - pi))
                for rpi in range(pi, row_end):
                    assembled_panels += "R_" + str(ri) + "_" + str(metric_idx+1) + "_P_" + str(rpi+1) \
                                    + " { gridPos: { h: 8, w: "+str(width)+", x: "+str(width*p)+", y: " \
                                    + str(r) + " }, }, \n"
                    p += 1
                    pi = rpi
                    if rpi + 1 == row_end:
                        pi = rpi + 1
                if pi >= len(metric.get('panels')):
                    break

    return assembled_panels


def get_alert_id(alert_channels, GRAFANA_API_KEY, GRAFANA_URL):
    grafana_notification_channel_uid = []
    api_url = GRAFANA_URL + "/api/alert-notifications/lookup"
    headers = {
        'Authorization': 'Bearer ' + GRAFANA_API_KEY,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    r = requests.get(api_url, headers=headers)
    r.raise_for_status()
    for g_data in r.json():
        if g_data["name"] in alert_channels:
            grafana_notification_channel_uid.append({"uid": g_data["uid"]})

    return (grafana_notification_channel_uid)


def parse_condition_query(condition_queries, targets):
    conditions = []
    ref_id_index = 64
    for t,_ in enumerate(targets):
        ref_id_index += 1
        if ref_id_index == ord("Z"):
            ref_id_index = ord("A")
        for condition_query in condition_queries:
            parts = condition_query.split(',')
            if len(parts) != 7:
                raise Exception('Condition query parameters not complete')
            if not int(parts[2]) == targets[t].get('ref_no'):
                continue
            ref_id = ref_id_index
            op = parts[0]
            if t == 0:
                op = 'WHEN'

            conditions.append({
                'operator_type': op,
                'reducer_type': parts[1],
                'query_ref_id': chr(ref_id),
                'query_time_end': parts[3],
                'query_time_start': parts[4],
                'evaluator_type': parts[5],
                'evaluator_params': parts[6],
                'reducer_params': [],
            })


    return conditions


def mkdir(path):
    if not os.path.isdir(path):
        os.makedirs(path)


def check_if_file_exists(path):
    if not os.path.exists(path):
        raise Exception("Unable to find the  file ", path)


def get_grafana_folder_id(grafana_folder_name, GRAFANA_API_KEY, GRAFANA_URL):
    api_url = GRAFANA_URL + "/api/folders"
    headers = {
        'Authorization': 'Bearer ' + GRAFANA_API_KEY,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    r = requests.get(api_url, headers=headers)
    r.raise_for_status()
    for g_data in r.json():
        if g_data["title"] == grafana_folder_name:
            return int(g_data["id"])

    return None


def create_grafana_folder(grafana_folder_name, GRAFANA_API_KEY, GRAFANA_URL):
    api_url = GRAFANA_URL + "/api/folders"
    headers = {
        'Authorization': 'Bearer ' + GRAFANA_API_KEY,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    data = {
        "title": grafana_folder_name
    }

    r = requests.post(api_url, headers=headers, data=json.dumps(data))
    r.raise_for_status()

    return (r["id"])

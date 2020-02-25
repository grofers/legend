#!/usr/bin/env python

import json
import os
import re
import subprocess
from git import Repo

from uuid import uuid4

from grafana_api.grafana_face import GrafanaFace

from .helpers.utilities import (
    assemble_panels_dynamic,
    jinja2_to_render,
    str_yaml_to_json,
    get_alert_id,
    parse_condition_query,
    get_grafana_folder_id,
    create_grafana_folder,
    mkdir
)

from . import (
    LEGEND_HOME,
    GRAFONNET_REPO_URL,
    GRAFONNET_REPO_NAME
)


make_abs_path = lambda d: os.path.join(
    os.path.dirname(os.path.abspath(__file__)), d)


def install_grafonnet_lib():
    legend_path = os.path.join(LEGEND_HOME)
    mkdir(legend_path)
    grafonnet_repo = os.path.join(
        LEGEND_HOME, GRAFONNET_REPO_NAME)
    grafonnet_path = os.path.join(
        LEGEND_HOME, GRAFONNET_REPO_NAME)
    if not os.path.isdir(grafonnet_path):
        try:
            repo = Repo.clone_from(GRAFONNET_REPO_URL, grafonnet_path)
        except Exception:
            raise ValueError("Error cloning grafonnet-lib folder from GitHub")
    else:
        try:
            # Update from master
            repo = Repo(grafonnet_path)
            repo.heads.master.checkout()
            repo.git.pull("origin", "master")
        except Exception:
            raise ValueError("Not a valid git repo/unable to pull master")
    pass


def convert_to_alnum(st):
    return re.sub(r'\W+', '', st)


def generate_jsonnet(input_dashboard, GRAFANA_API_KEY, GRAFANA_URL):
    component_description = {}

    if input_dashboard.get('alert_channels'):
        alert_ids = get_alert_id(
            input_dashboard['alert_channels'], GRAFANA_API_KEY, GRAFANA_URL)
        alert_service = input_dashboard['service']

    for component, values in input_dashboard['components'].items():

        template_str = jinja2_to_render(
                make_abs_path('metrics_library'),
                '{}_metrics.yaml'.format(component.lower()),
                data=values.get('dimensions',[])
        )
        templates = str_yaml_to_json(template_str)

        # Adding custom panels and adding custom alerts
        for template in templates:

            component_name = component
            if template.get('component') is not None:
                component_name = template.get('component')
            if component_description.get(component_name) is None:
                component_description[component_name] = {'reference': template.get('reference', ''),
                                                         'description': template.get('description', '')}

            tpanel_map = {x['title']: x for x in template['panels']}
            for panel in values.get('panels', []):
                if panel['title'] in tpanel_map.keys():
                    for k in panel.keys():
                        if k == 'alert_config':
                            try:
                                for ak in panel[k].keys():
                                    tpanel_map[panel['title']][k][ak] = panel[k][ak]
                            except KeyError:
                                tpanel_map[panel['title']][k] = panel[k]
                        else:
                            tpanel_map[panel['title']][k] = panel[k]
                else:
                    template['panels'].append(panel)

            for panel in template['panels']:
                panel['title_var'] = convert_to_alnum(panel['title'])
                for target in panel['targets']:
                    datasource_str = template['data_source'].lower()
                    render = jinja2_to_render(
                            make_abs_path('templates/datasource'),
                            '{}.j2'.format(datasource_str),
                            data=target
                    )
                    target['render'] = render
                panel['alertrender'] = ''

                if panel.get('alert_config'):
                    panel['alert_config']['rule']['name'] = panel['title']
                    panel['alert_config']['alert_ids'] = json.dumps(alert_ids)
                    panel['alert_config']['alert_service'] = alert_service
                    alertrender = jinja2_to_render(
                            make_abs_path('templates/alert'),
                            'alert.j2',
                            data=panel['alert_config']
                    )
                    if panel['alert_config'].get('condition_query'):
                        panel['alert_config']['conditions'] = parse_condition_query(
                                panel['alert_config']['condition_query'],
                                panel['targets']
                        )

                        for condition in panel['alert_config']['conditions']:
                            conditionrender = jinja2_to_render(
                                    make_abs_path('templates/alert'),
                                    'alert_condition.j2',
                                    data=condition
                            )
                            alertrender += conditionrender

                        panel['alertrender'] = alertrender

        if values.get('hide') is not None:
            if len(templates) > 0:
                templates[0]['hide'] = values.get('hide', None)
        if values.get('panels_in_row') is not None:
            if len(templates) > 0:
                templates[0]['panels_in_row'] = values.get('panels_in_row', None)
        values['metric'] = templates

    input_dashboard['component_desc'] = component_description
    input_dashboard['assemble_panels'] = assemble_panels_dynamic(input_dashboard)
    output = jinja2_to_render(make_abs_path('templates'), 'output.j2', data=input_dashboard)

    return output


def generate_dashboard_from_jsonnet(jsonnet_file_path):
    cmd_env_vars = dict(os.environ)
    grafonnet_lib = os.path.join(LEGEND_HOME, GRAFONNET_REPO_NAME)
    exec_command = 'jsonnet -J %s %s' % (grafonnet_lib, jsonnet_file_path)
    output = subprocess.check_output(
        exec_command.split(' '), env=cmd_env_vars
    )

    return output


def generate_dashboard_json(spec, GRAFANA_API_KEY, GRAFANA_URL):
    jsonnet = generate_jsonnet(spec, GRAFANA_API_KEY, GRAFANA_URL)
    jsonnet_tmp_path = os.path.join('/tmp', 'legend-%s.jsonnet' % uuid4())

    with open(jsonnet_tmp_path, 'w') as f:
        f.write(jsonnet)

    return json.loads(generate_dashboard_from_jsonnet(jsonnet_tmp_path))


def create_or_update_dashboard(auth, host, protocol, spec, dashboard_id=None):
    install_grafonnet_lib()
    grafana_api = GrafanaFace(auth=auth, host=host, protocol=protocol)

    GRAFANA_API_KEY = auth
    GRAFANA_URL = '%s://%s' % (protocol, host)

    dashboard_json = generate_dashboard_json(
        spec, GRAFANA_API_KEY, GRAFANA_URL)

    # Create dashboard based on the folder
    grafana_folder = spec['grafana_folder']

    grafana_folder_id = get_grafana_folder_id(
        grafana_folder, GRAFANA_API_KEY, GRAFANA_URL)
    if grafana_folder_id is None:
        grafana_folder_id = create_grafana_folder(
            grafana_folder, GRAFANA_API_KEY, GRAFANA_URL)

    dashboard_dict = {}
    dashboard_dict.update(dashboard=dashboard_json)
    dashboard_dict.update(folderId=int(grafana_folder_id))
    dashboard_dict.update(overwrite=True)

    resp = grafana_api.dashboard.update_dashboard(dashboard_dict)
    return resp


def delete_dashboard(auth, host, protocol, uid):
    grafana_api = GrafanaFace(auth=auth, host=host, protocol=protocol)

    return grafana_api.dashboard.delete_dashboard(dashboard_uid=uid)

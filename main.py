#!/usr/bin/env python

import argparse
import json
import os
import re
import subprocess


from helpers.utilities import (
        assemble_panels_dynamic,
        assemble_panels,
        jinja2_to_render,
        str_yaml_to_json,
        input_yaml_to_json,
        get_alert_id,
        parse_condition_query
)


def convert_to_alnum(str):
    return re.sub(r'\W+', '', str)


def template_builder(input):
    panel_dict = {}

    if input.get('alert_channels'):
        alert_ids = get_alert_id(input['alert_channels'])
        alert_service = input['service']

    for component, values in input['components'].items():

        panel_dict[component] = []

        template_str = jinja2_to_render(
                'metrics_library',
                '{}_metrics.yaml'.format(component.lower()),
                data=values.get('dimensions',[])
        )
        templates = str_yaml_to_json(template_str)

        # Adding custom panels and adding custom alerts
        for template in templates:
            tpanel_map = {x['title']: x for x in template['panels']}
            for panel in values.get('panels', []):
                if panel['title'] in tpanel_map.keys():
                    for k in panel.keys():
                        if k == 'alert_config':
                            try:
                                for ak in panel[k].keys():
                                        tpanel_map[panel['title']][k][ak] = panel[k][ak]
                            except:
                                tpanel_map[panel['title']][k] = panel[k]
                        else:
                            tpanel_map[panel['title']][k] = panel[k]
                else:
                    template['panels'].append(panel)

            for panel in template['panels']:
                panel['title_var'] = convert_to_alnum(panel['title'])
                panel_dict[component].append(panel['title_var'])
                for target in panel['targets']:
                    datasource_str = template['data_source'].lower()
                    render = jinja2_to_render(
                            'templates/datasource',
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
                            'templates/alert',
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
                                    'templates/alert',
                                    'alert_condition.j2',
                                    data=condition
                            )
                            alertrender += conditionrender

                        panel['alertrender'] = alertrender

        if values.get('hide') is not None:
            template['hide'] = values.get('hide', None)
        if values.get('panels_in_row') is not None:
            template['panels_in_row'] = values.get('panels_in_row', None)
        values['metric'] = templates

    input['assemble_panels'] = assemble_panels_dynamic(input)
    output = jinja2_to_render('templates', 'output.j2', data=input)
    return output


def generate_dashboard_from_jsonnet(path):
    cmd_env_vars = dict(os.environ)
    exec_command = 'jsonnet -J grafonnet-lib %s' % path
    output = subprocess.check_output(
        exec_command.split(' '), env=cmd_env_vars
    )

    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate dashboard with pre filled metrics'
    )
    parser.add_argument('-f', '--file', dest='input_file',
                        help='input file', required=True)
    args = parser.parse_args()

    input_file = args.input_file

    if not os.path.exists(input_file):
        raise Exception("Unable to find the file")

    input = input_yaml_to_json(input_file)
    jsonnet = template_builder(input)

    jsonnet_path = 'output.jsonnet'
    with open('output.jsonnet', 'w') as f:
        f.write(jsonnet)

    dashboard_json = generate_dashboard_from_jsonnet(jsonnet_path)
    with open('dashboard.json', 'w') as f:
        f.write(dashboard_json.decode('utf-8'))

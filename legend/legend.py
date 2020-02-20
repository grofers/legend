#!/usr/bin/env python

import json
import os
import re
import subprocess


from .helpers.utilities import (
    assemble_panels_dynamic,
    jinja2_to_render,
    str_yaml_to_json,
    input_yaml_to_json,
    get_alert_id,
    parse_condition_query
)

make_abs_path = lambda d: os.path.join(
    os.path.dirname(os.path.abspath(__file__)), d)


def convert_to_alnum(st):
    return re.sub(r'\W+', '', st)


def template_builder(input_dashboard):
    panel_dict = {}

    if input_dashboard.get('alert_channels'):
        alert_ids = get_alert_id(input_dashboard['alert_channels'])
        alert_service = input_dashboard['service']

    for component, values in input_dashboard['components'].items():

        panel_dict[component] = []

        template_str = jinja2_to_render(
                make_abs_path('metrics_library'),
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
                            except KeyError:
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

    input_dashboard['assemble_panels'] = assemble_panels_dynamic(input_dashboard)
    input_dashboard['grafonnet_path'] = os.environ['GRAFONNET_PATH']
    output = jinja2_to_render(make_abs_path('templates'), 'output.j2', data=input_dashboard)

    return output


def generate_dashboard_from_jsonnet(path):
    cmd_env_vars = dict(os.environ)
    exec_command = 'jsonnet -J grafonnet-lib %s' % path
    output = subprocess.check_output(
        exec_command.split(' '), env=cmd_env_vars
    )

    return output

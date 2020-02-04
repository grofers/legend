#!/usr/bin/env python

import argparse
import os
import re

from helpers.utilities import assemble_panels, jinja2_to_render, str_yaml_to_json, input_yaml_to_json, get_alert_id, parse_condition_query


def convert_to_alnum(str):
    return re.sub(r'\W+', '', str)


def template_builder(input):
    f = open("output.jsonnet", "w+")

    panel_dict = {}
    
    if input.get('alert_channels'):
        alert_ids = get_alert_id(input['alert_channels'])

    for component, values in input['components'].items():

        panel_dict[component] = []

        template_str = jinja2_to_render('metrics_library', '{}_metrics.yaml'.format(component.lower()), data=values)
        template = str_yaml_to_json(template_str)
        
        # Adding custom panels and adding custom alerts
        tpanel_map = {x['title']: x for x in template['panels']}
        for panel in values.get('panels', []):
            if panel['title'] in tpanel_map.keys():
                for k in panel.keys():
                    if k == 'alert_config':
                        for ak in panel[k].keys():
                            tpanel_map[panel['title']][k][ak] = panel[k][ak]
                    else:
                        tpanel_map[panel['title']][k] = panel[k]
            else:
                template['panels'].append(panel)

        for panel in template['panels']:
            panel['title_var'] = convert_to_alnum(panel['title'])
            panel_dict[component].append(panel['title_var'])
            for target in panel['targets']:
                datasource_str = template['data_source'].lower()
                render = jinja2_to_render('templates/datasource', '{}.j2'.format(datasource_str),
                                          data=target)
                target['render'] = render
            panel['alertrender'] = ''
            # if alert is present then render it
            # import pdb; pdb.set_trace()
            if panel.get('alert_config') :
                panel['alert_config']['rule']['name'] = panel['title']
                panel['alert_config']['alert_ids'] = alert_ids
                alertrender = jinja2_to_render(
                        'templates/alert',
                        'alert.j2',
                        data=panel['alert_config']
                )
                if panel['alert_config'].get('condition_query'):
                    panel['alert_config']['conditions'] = parse_condition_query(
                            panel['alert_config']['condition_query']
                    )

                for condition in panel['alert_config']['conditions']:
                    conditionrender = jinja2_to_render('templates/alert', 'alert_condition.j2',
                                        data=condition)
                    alertrender += conditionrender
                
                panel['alertrender'] = alertrender
            

        values['metric'] = template

    input['assemble_panels'] = assemble_panels(panel_dict)

    output = jinja2_to_render('templates', 'output.j2', data=input)
    f.write(output)

    f.close()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Generate dashboard with pre filled metrics')
    parser.add_argument('-f', '--file', dest='input_file',
                        help='input file', required=True)
    args = parser.parse_args()

    input_file = args.input_file

    if not os.path.exists(input_file):
        raise Exception("Unable to find the file")

    input = input_yaml_to_json(input_file)
    template_builder(input)

#!/usr/bin/env python

import argparse
import os
import re

from helpers.utilities import assemble_panels, jinja2_to_render, str_yaml_to_json, input_yaml_to_json


def convert_to_alnum(str):
    return re.sub(r'\W+', '', str)


def template_builder(input):
    f = open("output.jsonnet", "w+")

    panel_dict = {}

    for component, values in input['Components'].items():

        panel_dict[component] = []

        template_str = jinja2_to_render('metrics_library', '{}_metrics.yaml'.format(component.lower()), data=values)
        template = str_yaml_to_json(template_str)

        for panel in template['Panels']:
            panel['title_var'] = convert_to_alnum(panel['Title'])
            panel_dict[component].append(panel['title_var'])
            for target in panel['Targets']:
                datasource_str = template['Datasource'].lower()
                render = jinja2_to_render('templates/datasource', '{}.j2'.format(datasource_str),
                                          data=target)
                target['render'] = render

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

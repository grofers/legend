#!/usr/bin/env python

import argparse
import os
import re

from helpers.utilities import ASSEMBLE_PANELS, JINJA2_TO_RENDER, STR_YAML_TO_JSON, INPUT_YAML_TO_JSON


def convert_to_alnum(str):
    return re.sub(r'\W+', '', str)


def template_builder(input):
    f = open("output.jsonnet", "w+")

    panel_dict = {}

    for component, values in input['Components'].items():

        panel_dict[component] = []

        template_str = JINJA2_TO_RENDER('metrics_library', '{}_metrics.yaml'.format(component.lower()), data=values)
        template = STR_YAML_TO_JSON(template_str)

        for panel in template['Panels']:
            panel['title_var'] = convert_to_alnum(panel['Title'])
            panel_dict[component].append(panel['title_var'])
            for target in panel['Targets']:
                datasource_str = template['Datasource'].lower()
                render = JINJA2_TO_RENDER('templates/datasource', '{}.j2'.format(datasource_str),
                                          data=target)
                target['render'] = render

        values['metric'] = template

    input['assemble_panels'] = ASSEMBLE_PANELS(panel_dict)

    output = JINJA2_TO_RENDER('templates', 'output.j2', data=input)
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

    input = INPUT_YAML_TO_JSON(input_file)
    template_builder(input)

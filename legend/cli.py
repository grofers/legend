#!/usr/bin/env python

import argparse
import os

from .legend import template_builder
from .legend import generate_dashboard_from_jsonnet


from .helpers.utilities import input_yaml_to_json


def main():
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

if __name__ == '__main__':
    main()

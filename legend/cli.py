#!/usr/bin/env python

import argparse
import os

from .legend import create_or_update_dashboard


from .helpers.utilities import input_yaml_to_json

GRAFANA_API_KEY = os.environ['GRAFANA_API_KEY']
GRAFANA_HOST = os.environ['GRAFANA_HOST']
GRAFANA_PROTOCOL = os.environ['GRAFANA_PROTOCOL']


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
    print(create_or_update_dashboard(GRAFANA_API_KEY, GRAFANA_HOST,
                                     GRAFANA_PROTOCOL, input))


if __name__ == '__main__':
    main()

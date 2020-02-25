#!/usr/bin/env python

import argparse
import os
import configparser

from .legend import create_or_update_dashboard

from .helpers.utilities import (
    input_yaml_to_json
)


def main():

    parser = argparse.ArgumentParser(
        description='Generate dashboard with pre filled metrics'
    )
    parser.add_argument('-f', '--file', dest='input_file',
                        help='input file', required=True)
    parser.add_argument('-c', '--config', dest='input_config', default='legend.cfg',
                        help='input configuration', required=False)

    args = parser.parse_args()

    input_file = args.input_file
    input_config = args.input_config

    if not os.path.exists(input_file):
        raise Exception("Unable to find the file")

    if input_config is not None:
        if not os.path.exists(input_config):
            raise Exception("Unable to find the configuration file")
        config = configparser.SafeConfigParser()
        config.read(input_config)
        GRAFANA_API_KEY = config.get('grafana', 'api_key')
        GRAFANA_PROTOCOL = config.get('grafana', 'protocol')
        GRAFANA_HOST = config.get('grafana', 'host')

    if os.environ.get('GRAFANA_API_KEY') is not None:
        GRAFANA_API_KEY = os.environ['GRAFANA_API_KEY']
    if os.environ.get('GRAFANA_HOST') is not None:
        GRAFANA_HOST = os.environ['GRAFANA_HOST']
    if os.environ.get('GRAFANA_PROTOCOL') is not None:
        GRAFANA_PROTOCOL = os.environ['GRAFANA_PROTOCOL']

    spec = input_yaml_to_json(input_file)
    print(create_or_update_dashboard(GRAFANA_API_KEY, GRAFANA_HOST,
                                     GRAFANA_PROTOCOL, spec))


if __name__ == '__main__':
    main()

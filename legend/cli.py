#!/usr/bin/env python

import os
from urllib.parse import urljoin
import json
import click

from .legend import (
    generate_jsonnet,
    generate_dashboard_from_jsonnet,
    create_or_update_grafana_dashboard,
)

from .configure import install_grafonnet_lib, load_legend_config
from .helpers.utilities import check_if_file_exists, input_yaml_to_json

from .metrics_library import schema


def publish_main():
    pass


@click.group()
def cli_main():

    """
    Build and publish Grafana dashboards for your services with prefilled
    metrics and alerts for your services

    You need a valid API key for Grafana for the tool to work.
    """
    pass


@cli_main.command()
@click.option("-c", "--config_file", help="confoguration file for legend")
def configure(config_file):
    if config_file is not None:
        check_if_file_exists(config_file)
    install_grafonnet_lib()
    legend_config = load_legend_config(config_file=config_file)


@cli_main.command()
@click.argument("input_file", required=True, type=click.Path())
@click.option("-c", "--config_file", help="configuration file for legend")
@click.option(
    "-s",
    "--silent",
    is_flag=True,
    help="do not print the generated dashboard to stdout",
)
@click.option("-o", "--output_file", help="output file to store generated json")
def build(input_file, config_file, silent, output_file):
    check_if_file_exists(input_file)
    legend_config = load_legend_config(config_file=config_file)
    input_spec = input_yaml_to_json(schema, input_file)
    jsonnet_file = generate_jsonnet(input_spec, legend_config)
    dashboard_json = generate_dashboard_from_jsonnet(jsonnet_file)
    if not silent:
        click.echo("%s" % json.dumps(dashboard_json))
    if output_file is not None:
        with open(output_file, "w") as f:
            f.write(json.dumps(dashboard_json))


@cli_main.command()
@click.argument("input_json", required=True, type=click.Path())
@click.option(
    "-f",
    "--grafana_folder",
    required=True,
    help="folder in grafana to publish the dashboard",
)
@click.option("-c", "--config_file", help="configuration file for legend")
def publish(input_json, grafana_folder, config_file):
    check_if_file_exists(input_json)
    legend_config = load_legend_config(config_file=config_file)
    with open(input_json) as json_data:
        dashboard_json = json.load(json_data)
    resp = create_or_update_grafana_dashboard(
        dashboard_json, legend_config, str(grafana_folder)
    )

    grafana_url = urljoin(
        "%s://%s" % (legend_config["grafana_protocol"], legend_config["grafana_host"]),
        resp["url"],
    )

    click.echo("Dashboard built and applied! %s" % grafana_url)


@cli_main.command()
@click.argument("input_file", type=click.Path())
@click.option("-c", "--config_file", help="configuration file for legend")
def apply(input_file, config_file):
    check_if_file_exists(input_file)
    legend_config = load_legend_config(config_file=config_file)
    input_spec = input_yaml_to_json(schema, input_file)
    jsonnet_file = generate_jsonnet(input_spec, legend_config)
    dashboard_json = generate_dashboard_from_jsonnet(jsonnet_file)
    resp = create_or_update_grafana_dashboard(
        dashboard_json, legend_config, str(input_spec["grafana_folder"])
    )

    grafana_url = urljoin(
        "%s://%s" % (legend_config["grafana_protocol"], legend_config["grafana_host"]),
        resp["url"],
    )

    click.echo("Dashboard built and applied! %s" % grafana_url)

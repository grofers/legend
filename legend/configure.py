#!/usr/bin/env python

import json
import os
import configparser

from git import Repo

from .helpers.utilities import (
    mkdir
)

from . import (
    LEGEND_HOME,
    GRAFONNET_REPO_URL,
    GRAFONNET_REPO_NAME,
    LEGEND_DEFAULT_CONFIG,
    GRAFONNET_REPO_RELEASE_TAG,
)


def set_global_vars():
    if os.environ.get("LEGEND_HOME") is not None:
        LEGEND_HOME = os.environ.get("LEGEND_HOME")

    if os.environ.get("GRAFONNET_REPO_NAME") is not None:
        GRAFONNET_REPO_NAME = os.environ.get("GRAFONNET_REPO_NAME")

    if os.environ.get("GRAFONNET_REPO_URL") is not None:
        GRAFONNET_REPO_URL = os.environ.get("GRAFONNET_REPO_URL")
    
    if os.environ.get("GRAFONNET_REPO_RELEASE_TAG") is not None:
        GRAFONNET_REPO_RELEASE_TAG = os.environ.get("GRAFONNET_REPO_RELEASE_TAG")

def install_grafonnet_lib():
    set_global_vars()
    legend_path = os.path.join(LEGEND_HOME)
    mkdir(legend_path)
    grafonnet_path = os.path.join(LEGEND_HOME, GRAFONNET_REPO_NAME)
    if not os.path.isdir(grafonnet_path):
        try:
            repo = Repo.clone_from(GRAFONNET_REPO_URL, grafonnet_path)
            repo.git.checkout(GRAFONNET_REPO_RELEASE_TAG)
        except Exception:
            raise ValueError("Error cloning grafonnet-lib folder from GitHub")
    else:
        try:
            # Update from the chosen release
            repo = Repo(grafonnet_path)
            repo.git.checkout(GRAFONNET_REPO_RELEASE_TAG)
            repo.git.pull("origin", GRAFONNET_REPO_RELEASE_TAG)
        except Exception:
            raise ValueError("Not a valid git repo/unable to pull {release_tag}".format(release_tag=GRAFONNET_REPO_RELEASE_TAG))
    return ()


def load_legend_config(config_file=None):
    set_global_vars()
    config = configparser.SafeConfigParser()

    # Load config from provided input file
    legend_config = {}
    if config_file is not None:
        configuration = config.read(config_file)
        legend_config.update(grafana_api_key=config.get("grafana", "api_key"))
        legend_config.update(grafana_host=config.get("grafana", "host"))
        legend_config.update(
            grafana_protocol=config.get("grafana", "protocol"))

    # Load config from LEGEND_HOME
    elif os.path.exists(os.path.join(LEGEND_HOME, LEGEND_DEFAULT_CONFIG)):
        configuration = config.read(os.path.join(
            LEGEND_HOME, LEGEND_DEFAULT_CONFIG))
        legend_config.update(grafana_api_key=config.get("grafana", "api_key"))
        legend_config.update(grafana_host=config.get("grafana", "host"))
        legend_config.update(
            grafana_protocol=config.get("grafana", "protocol"))

    # Override with environment variables if any
    if os.environ.get("GRAFANA_API_KEY") is not None:
        legend_config.update(grafana_api_key=os.environ["GRAFANA_API_KEY"])
    if os.environ.get("GRAFANA_HOST") is not None:
        legend_config.update(grafana_host=os.environ["GRAFANA_HOST"])
    if os.environ.get("GRAFANA_PROTOCOL") is not None:
        legend_config.update(grafana_protocol=os.environ["GRAFANA_PROTOCOL"])

    if None not in legend_config.values():
        return legend_config
    else:
        raise Exception(
            "Incomplete legend config, please update the legend config file or set env values"
        )

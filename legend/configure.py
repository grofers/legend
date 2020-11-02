#!/usr/bin/env python

import json
import os
import configparser

from git import Repo

from .helpers.utilities import mkdir

from . import (
    LEGEND_HOME,
    GRAFONNET_REPO_URL,
    GRAFONNET_REPO_NAME,
    LEGEND_DEFAULT_CONFIG,
    GRAFONNET_REPO_RELEASE_TAG,
    GRAFANA_DEFAULT_DATA_SOURCES,
)


def install_grafonnet_lib():
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
    config = configparser.SafeConfigParser()

    # Read config from provided input file
    legend_config = {}
    if config_file is not None:
        config.read(config_file)

    # Read config from LEGEND_HOME
    elif os.path.exists(os.path.join(LEGEND_HOME, LEGEND_DEFAULT_CONFIG)):
        config.read(os.path.join(LEGEND_HOME, LEGEND_DEFAULT_CONFIG))

    # Load the config. If any of the config value is present in env variables then, load from there instead
    legend_config.update(grafana_api_key=os.environ.get("GRAFANA_API_KEY", config.get("grafana", "api_key", fallback=None)))
    legend_config.update(grafana_host=os.environ.get("GRAFANA_HOST", config.get("grafana", "host", fallback=None)))
    legend_config.update(grafana_protocol=os.environ.get("GRAFANA_PROTOCOL", config.get("grafana", "protocol", fallback=None)))

    if None not in legend_config.values():
        return legend_config
        
    raise Exception("Incomplete legend config, please update the legend config file or set env values")

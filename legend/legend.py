#!/usr/bin/env python

import json
import os
import subprocess

from uuid import uuid4

from grafana_api.grafana_face import GrafanaFace

from .helpers.utilities import (
    assemble_panels_dynamic,
    convert_to_alnum,
    jinja2_to_render,
    str_yaml_to_json,
    get_alert_id,
    parse_condition_query,
    get_grafana_folder_id,
    create_grafana_folder,
    mkdir,
)

from .configure import (
    set_global_vars
)
from . import (
    LEGEND_HOME,
    GRAFONNET_REPO_NAME,
    LEGEND_DEFAULT_CONFIG,
)

make_abs_path = lambda d: os.path.join(os.path.dirname(os.path.abspath(__file__)), d)

global LEGEND_HOME
global GRAFONNET_REPO_NAME


def generate_jsonnet(input_spec, legend_config):
    grafana_api_key = legend_config["grafana_api_key"]
    grafana_url = "%s://%s" % (
        legend_config["grafana_protocol"],
        legend_config["grafana_host"],
    )

    component_description = {}
    if input_spec.get("alert_channels"):
        alert_ids = get_alert_id(
            input_spec["alert_channels"], grafana_api_key, grafana_url
        )
        alert_service = input_spec["service"]

    for component, values in input_spec["components"].items():

        template_str = jinja2_to_render(
            make_abs_path("metrics_library"),
            "{}_metrics.yaml".format(component.lower()),
            data=values.get("dimensions", []),
        )
        templates = str_yaml_to_json(template_str)

        # Adding custom panels and adding custom alerts
        for template in templates:

            component_name = component
            if template.get("component") is not None:
                component_name = template.get("component")
            if component_description.get(component_name) is None:
                component_description[component_name] = {
                    "reference": template.get("reference", ""),
                    "description": template.get("description", ""),
                }

            tpanel_map = {x["title"]: x for x in template["panels"]}
            for panel in values.get("panels", []):
                if panel["title"] in tpanel_map.keys():
                    for k in panel.keys():
                        if k == "alert_config":
                            try:
                                for ak in panel[k].keys():
                                    tpanel_map[panel["title"]][k][ak] = panel[k][ak]
                            except KeyError:
                                tpanel_map[panel["title"]][k] = panel[k]
                        else:
                            tpanel_map[panel["title"]][k] = panel[k]
                else:
                    template["panels"].append(panel)

            for panel in template["panels"]:
                panel["title_var"] = convert_to_alnum(panel["title"])
                for target in panel["targets"]:
                    datasource_str = template["data_source"].lower()
                    render = jinja2_to_render(
                        make_abs_path("templates/datasource"),
                        "{}.j2".format(datasource_str),
                        data=target,
                    )
                    target["render"] = render
                panel["alertrender"] = ""

                if panel.get("alert_config") is not None:
                    panel["alert_config"]["rule"]["name"] = panel["title"]
                    panel["alert_config"]["alert_ids"] = json.dumps(alert_ids)
                    panel["alert_config"]["alert_service"] = alert_service
                    alertrender = jinja2_to_render(
                        make_abs_path("templates/alert"),
                        "alert.j2",
                        data=panel["alert_config"],
                    )
                    if panel["alert_config"].get("condition_query"):
                        panel["alert_config"]["conditions"] = parse_condition_query(
                            panel["alert_config"]["condition_query"], panel["targets"]
                        )

                        for condition in panel["alert_config"]["conditions"]:
                            conditionrender = jinja2_to_render(
                                make_abs_path("templates/alert"),
                                "alert_condition.j2",
                                data=condition,
                            )
                            alertrender += conditionrender

                        panel["alertrender"] = alertrender

        if values.get("hide") is not None:
            if len(templates) > 0:
                templates[0]["hide"] = values.get("hide", None)
        if values.get("panels_in_row") is not None:
            if len(templates) > 0:
                templates[0]["panels_in_row"] = values.get("panels_in_row", None)
        values["metric"] = templates

    input_spec["component_desc"] = component_description
    input_spec["assemble_panels"] = assemble_panels_dynamic(input_spec)
    output = jinja2_to_render(make_abs_path("templates"), "output.j2", data=input_spec)

    jsonnet_tmp_path = os.path.join("/tmp", "legend-%s.jsonnet" % uuid4())

    with open(jsonnet_tmp_path, "w") as f:
        f.write(output)
        print("tempfile : ", jsonnet_tmp_path)

    return jsonnet_tmp_path


def generate_dashboard_from_jsonnet(jsonnet_file_path):
    set_global_vars()
    cmd_env_vars = dict(os.environ)
    grafonnet_lib = os.path.join(LEGEND_HOME, GRAFONNET_REPO_NAME)
    exec_command = "jsonnet -J %s %s" % (grafonnet_lib, jsonnet_file_path)
    output = subprocess.check_output(exec_command.split(" "), env=cmd_env_vars)
    return json.loads(output)


def create_or_update_grafana_dashboard(
    dashboard_json, legend_config, dashboard_id=None
):

    auth = legend_config["grafana_api_key"]
    host = legend_config["grafana_host"]
    protocol = legend_config["grafana_protocol"]
    grafana_url = "%s://%s" % (protocol, host)

    grafana_api = GrafanaFace(auth=auth, host=host, protocol=protocol)

    # Create dashboard based on the folder, if a new dashboard
    # Check if the folder exists
    id = get_grafana_folder_id(dashboard_id, auth, grafana_url)
    if id is None:
        # Create folder if doesn't exist
        id = create_grafana_folder(dashboard_id, auth, grafana_url)

    dashboard_dict = {}
    dashboard_dict.update(dashboard=dashboard_json)
    dashboard_dict.update(folderId=int(id))
    dashboard_dict.update(overwrite=True)

    resp = grafana_api.dashboard.update_dashboard(dashboard_dict)

    return resp


def delete_dashboard(legend_config, uid):
    auth = legend_config["grafana_api_key"]
    host = legend_config["grafana_host"]
    protocol = legend_config["grafana_protocol"]

    grafana_api = GrafanaFace(auth=auth, host=host, protocol=protocol)

    return grafana_api.dashboard.delete_dashboard(dashboard_uid=uid)

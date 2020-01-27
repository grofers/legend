#!/usr/bin/env python

import sys
import argparse
import os
import yaml
from jinja2 import Template
import helpers


def dashboard_builder(input):

    # Create an ouput file to write the jsonnet config
    f = open("output.jsonnet", "w+")

    # Imports
    imports = helpers.constants.IMPORTS
    f.write(imports+"\n")

    # Build individual panels for each component
    panels_constants = {}
    panels_list = {}
    component_ref = {}
    for component in input['Components']:
        ComponentIdentifiers = input['Components'][component]
        ServiceEnvironment = input["Environment"]
        AlertChannels = input["AlertChannels"]
        panels_constants[component], panels_list[component], component_ref[component] = helpers.generators.add_component(
            component, ComponentIdentifiers,
            ServiceEnvironment,  AlertChannels)

    # Write constants to the output file
    for data in panels_constants.values():
        for k, v in data.items():
            f.write("local "+k+" = "+v+"; \n")

    # Build service description panel
    service_template = Template(helpers.constants.SERVICE_DESC)
    msg = service_template.render(SERVICE_DESC_INDIVIDUAL_COMPONENTS=component_ref.values(),
                                  service=input["Title"], references=input["References"])
    sdp = helpers.constants.TEXT_PANEL.format(
        title="Service Description", content=msg)

    # Placehoplder to avoid \n by python,
    # if we add additional \ then JSONNET would throuw an error step
    sdp = sdp.replace("<placeHolder>", "")
    f.write("local sdp = "+sdp+"; \n")

    # Write data to the sheet
    head = helpers.constants.DASHBOARD_HEAD.format(
        title=str(input['Title'] + " - " + input["Environment"]),
        tags=input['Tags'])
    f.write(head+"\n")

    # Write the service desc panel gridPos
    f.write(
        ".addPanels([ sdp { gridPos: { h: 10, w: 15, x: 0, y: 0 },},])"+"\n")

    # Assemble the panels and write to sheet (the gridPOS panels )
    assembled_panels = helpers.utilities.ASSEMBLE_PANELS(panels_list)
    f.write(assembled_panels+"\n")

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

    input = helpers.utilities.INPUT_YAML_TO_JSON(input_file)
    dashboard_builder(input)

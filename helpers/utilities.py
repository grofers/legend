#!/usr/bin/env python

import yaml
from jinja2 import Environment, FileSystemLoader


def INPUT_YAML_TO_JSON(input_file):
    with open(input_file, 'r') as stream:
        try:
            return (yaml.load(stream))
        except yaml.YAMLError as exc:
            raise Exception(exc)


def STR_YAML_TO_JSON(str):
    try:
        return (yaml.load(str))
    except yaml.YAMLError as exc:
        raise Exception(exc)


def JINJA2_TO_RENDER(directory, filename, data):
    file_loader = FileSystemLoader(directory)
    env = Environment(loader=file_loader)
    template = env.get_template(filename)
    return template.render(data=data)


def ASSEMBLE_PANELS(panels_dict):
    assemble_panels = ''

    n = 1
    for k, v in panels_dict.items():
        assemble_panels += k + \
                           "  { gridPos: { h: 4, w: 24, x: 0, y: " + str(n) + " }, }, \n"
        n += 1
        for i in range(0, len(v), 2):
            try:
                assemble_panels += str(v[i]) \
                                   + " { gridPos: { h: 8, w: 12, x: 0, y: " \
                                   + str(n) + " }, }, \n" \
                                   + v[i + 1] \
                                   + " { gridPos: { h: 8, w: 12, x: 12, y: " \
                                   + str(n) + " }, }, \n"
            except IndexError as e:
                assemble_panels += v[i] + \
                                   "  { gridPos: { h: 8, w: 12, x: 0, y: " + \
                                   str(n) + " }, }, \n"
            n += 1

    return (assemble_panels)

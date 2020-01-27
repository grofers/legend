#!/usr/bin/env python

import sys
import os
import yaml


def INPUT_YAML_TO_JSON(input_file):
    with open(input_file, 'r') as stream:
        try:
            return (yaml.load(stream))
        except yaml.YAMLError as exc:
            raise Exception(exc)


def ASSEMBLE_PANELS(panels_list):
    assemble_panels = '''
    .addPanels(
  [
    '''

    n = 1
    for component_panel in panels_list.values():
        for k, v in component_panel.items():
            assemble_panels += k + \
                "  { gridPos: { h: 4, w: 24, x: 0, y: "+str(n)+" }, }, \n"
            n += 1
            for i in range(0, len(v), 2):
                try:
                    assemble_panels += str(v[i]) \
                        + " { gridPos: { h: 8, w: 12, x: 0, y: " \
                        + str(n)+" }, }, \n" \
                        + v[i+1] \
                        + " { gridPos: { h: 8, w: 12, x: 12, y: " \
                        + str(n)+" }, }, \n"
                except IndexError as e:
                    assemble_panels += v[i] + \
                        "  { gridPos: { h: 8, w: 12, x: 0, y: " + \
                        str(n)+" }, }, \n"
                n += 1
    assemble_panels_close = '''
  ]
)
'''
    assemble = assemble_panels + assemble_panels_close

    return (assemble)

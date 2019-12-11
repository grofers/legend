#!/usr/bin/env python
 
import sys 
import argparse
import os
import yaml
import helpers
from jinja2 import Template

#TODO: Add promethus and influx DB metrics as samples at least
#TODO: Add Description of serice at the top 
#TODO: seperate the head and the templates

def dashboard_builder(input):
    #Create an ouput file to write the jsonnet config
    f = open("output.jsonnet","w+")

    #Imports 
    imports = helpers.constants.IMPORTS
    f.write(imports+"\n")

    #Build individual panels for each component
    panels_constants = {}
    panels_list = {}
    for component in input['Components']:
        InputIdentifierKeys = input['Components'][component]
        panels_constants[component],panels_list[component] = helpers.generators.ADD_COMPONENT(component,InputIdentifierKeys)
        
    #Write constants to the output file
    for data in panels_constants.values():
        for k,v in data.items():
            f.write("local "+k+" = "+v+"; \n")

    #Write data to the sheet
    head = helpers.generators.DASHBOARD_HEAD(input['Title'],input['Tags'],input['Description'],input["Environment"])
    f.write(head+"\n")

    #Assemble the panels and write to sheet
    assembled_panels = helpers.subtasks.ASSEMBLE_PANELS(panels_list)
    f.write(assembled_panels+"\n")

    f.close()

if __name__ == '__main__':
   
    parser = argparse.ArgumentParser(description='Generate dashboard with pre filled metrics')
    parser.add_argument('-f','--file', dest='input_file', help='input file', required=True)
    args = parser.parse_args()
    
    input_file = args.input_file

    if not os.path.exists(input_file):
        raise Exception ("Unable to find the file")

    input = helpers.subtasks.INPUT_YAML_TO_JSON(input_file)
    dashboard_builder(input)
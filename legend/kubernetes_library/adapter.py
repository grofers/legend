import os
import os.path
import sys


def kubernetes_library_eval(component_name, arg):
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    sys.path.append(BASE_DIR)
    module = __import__(component_name)
    func = getattr(module, "run")
    func(arg)


def kubernetes_library_component_exists(component_name):
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    if os.path.isfile("{}/{}.py".format(BASE_DIR, component_name)) == True:
        return True
    return False

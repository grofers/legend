from kubernetes import client, config, utils
import yaml

def slo_component(body):
    config.load_kube_config()
    v1 = client.CustomObjectsApi()
    v1.create_namespaced_custom_object(
        group="monitoring.spotahome.com",
        version="v1alpha1",
        namespace="monitoring",
        plural="servicelevels",
        body=yaml.load(body, Loader=yaml.FullLoader)
    )

function_mapping = {
  "slo": slo_component,
}

def kubernetes_library_eval(function_name, arg):
    function = function_mapping[function_name]
    function(arg)

def kubernetes_library_component_exists(component_name):
    print("Checking if component is a kubernetes component")
    print(component_name)
    if component_name in function_mapping:
        return True
    print("No component found")
    return False

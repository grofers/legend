############
#
# Constants
#
############

# Grafana DB
# Grafana API readonly key, hence plain text
GRAFANA_API_KEY = ""
GRAFANA_URL = "https://grafana.grofers.com/api"

try:
    from helpers.local_constants import *
except:
    pass
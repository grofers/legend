import os
############
#
# Constants
#
############

# Grafana DB
# Grafana API readonly key, hence plain text
GRAFANA_API_KEY = os.environ.get('GRAFANA_API_KEY', '')
GRAFANA_URL = "https://grafana.grofers.com/api"

import os
############
#
# Constants
#
############

import os


# Grafana DB
# Grafana API readonly key, hence plain text
GRAFANA_API_KEY = os.environ.get('GRAFANA_API_KEY', '')
GRAFANA_URL = '%s://%s/api' % (os.environ.get('GRAFANA_PROTOCOL'),
                               os.environ.get('GRAFANA_HOST'))

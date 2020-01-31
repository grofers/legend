############
#
# Constants
#
############

# Grafana DB
# Grafana API readonly key, hence plain text
GRAFANA_API_KEY = ""
GRAFANA_URL = "https://grafana.grofers.com/api"

############
#
# Alerts and monitoring
#
############

ADD_ALERT = '''
.addAlert(
      '{rule_name}',
      executionErrorState='alerting',
      forDuration='{forDuration}',
      frequency='{evaluate_every}',
      handler=1,
      message='Severity: {severity}',
      noDataState='no_data',
      notifications={AlertChannels},
    )
'''
ADD_ALERT_CONDITION = '''
.addCondition(
    alertCondition.new(
        evaluatorParams=[{evaluatorParams}],
        evaluatorType='{evaluatorType}',
        operatorType='{operatorType}',
        queryRefId='{queryRefId}',
        queryTimeEnd='{queryTimeEnd}',
        queryTimeStart='{queryTimeStart}',
        reducerParams={reducerParams},
        reducerType='{reducerType}',
    )
)
'''

from helpers.local_constants import *
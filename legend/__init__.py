import os
import sentry_sdk

sentry_sdk.init(traces_sample_rate=1.0)

LEGEND_HOME_NAME = ".legend"
LEGEND_DEFAULT_CONFIG = "legend.cfg"

LEGEND_HOME = os.environ.get("LEGEND_HOME", os.path.join(os.path.expanduser("~"), LEGEND_HOME_NAME))

GRAFONNET_REPO_URL = "https://github.com/grafana/grafonnet-lib"
GRAFONNET_REPO_NAME = "grafonnet-lib"
GRAFONNET_REPO_RELEASE_TAG = "v0.1.0"

GRAFANA_DEFAULT_DATA_SOURCES = {
    "PROMETHEUS": os.environ.get("GRAFANA_DEFAULT_PROMETHEUS_DATA_SOURCE"),
    "INFLUXDB": os.environ.get("GRAFANA_DEFAULT_INFLUXDB_DATA_SOURCE"),
    "CLOUDWATCH": os.environ.get("GRAFANA_DEFAULT_CLOUDWATCH_DATA_SOURCE"),
    "LOKI": os.environ.get("GRAFANA_DEFAULT_LOKI_DATA_SOURCE"),
}

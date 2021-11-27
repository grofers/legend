import os
import sentry_sdk

sentry_sdk.init(traces_sample_rate=1.0)

LEGEND_HOME_NAME = ".legend"
LEGEND_DEFAULT_CONFIG = "legend.cfg"

LEGEND_HOME = os.getenv(
    "LEGEND_HOME", os.path.join(os.path.expanduser("~"), LEGEND_HOME_NAME)
)

GRAFONNET_REPO_URL = os.getenv(
    "GRAFFONNET_REPO_URL", "https://github.com/grafana/grafonnet-lib"
)
GRAFONNET_REPO_NAME = os.getenv("GRAFONNET_REPO_NAME", "grafonnet-lib")
# Switching release tag to master because there has been no new release for a very long time and we needed fixes from newer commits.
# https://github.com/grafana/grafonnet-lib/commit/82ccf9013f14d976b83a01a43f5f062019cbee2c
GRAFONNET_REPO_RELEASE_TAG = os.getenv("GRAFONNET_REPO_RELEASE_TAG", "master")

GRAFANA_DEFAULT_DATA_SOURCES = {
    "PROMETHEUS": os.environ.get("GRAFANA_DEFAULT_PROMETHEUS_DATA_SOURCE"),
    "INFLUXDB": os.environ.get("GRAFANA_DEFAULT_INFLUXDB_DATA_SOURCE"),
    "CLOUDWATCH": os.environ.get("GRAFANA_DEFAULT_CLOUDWATCH_DATA_SOURCE"),
    "LOKI": os.environ.get("GRAFANA_DEFAULT_LOKI_DATA_SOURCE"),
}

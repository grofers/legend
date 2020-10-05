import os
import sentry_sdk

sentry_sdk.init(
    traces_sample_rate=1.0
)

LEGEND_HOME_NAME = ".legend"
LEGEND_DEFAULT_CONFIG = "legend.cfg"

LEGEND_HOME = os.environ.get(
    "LEGEND_HOME", os.path.join(os.path.expanduser("~"), LEGEND_HOME_NAME)
)

GRAFONNET_REPO_URL = "https://github.com/grafana/grafonnet-lib"
GRAFONNET_REPO_NAME = "grafonnet-lib"
GRAFONNET_REPO_RELEASE_TAG = "v0.1.0"

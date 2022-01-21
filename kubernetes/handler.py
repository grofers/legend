import logging
import os

import kopf

from urllib.parse import urljoin

from legend.legend import (
    delete_dashboard,
    generate_jsonnet,
    generate_dashboard_from_jsonnet,
    create_or_update_grafana_dashboard,
)

from legend.helpers.validations import validate_input

from legend.configure import load_legend_config, install_grafonnet_lib

from legend.metrics_library import schema

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
DEV = os.environ.get("DEV", False)

logging.basicConfig(
    format="%(module)s [%(levelname)s] %(message)s", level=getattr(logging, LOG_LEVEL)
)
logger = logging.getLogger(__name__)
logger.setLevel(getattr(logging, LOG_LEVEL))

logger.info(
    "Starting grafana-dashboards operator to create and manage grafana dashboards"
)

if DEV:
    logger.info("Start in DEV mode")
    from dev import login_handler

# Installing grafonnetlib for crd
install_grafonnet_lib()


def create_or_update_handler(spec, name, **kwargs):
    body = kwargs["body"]
    spec = body["spec"]["grafana_dashboard_spec"]

    validate_input(schema, spec)
    legend_config = load_legend_config()
    jsonnet_file = generate_jsonnet(spec, legend_config)
    dashboard_json = generate_dashboard_from_jsonnet(jsonnet_file)
    dashboard_id = str(spec["grafana_folder"])
    resp = create_or_update_grafana_dashboard(
        dashboard_json, legend_config, dashboard_id
    )

    host = legend_config["grafana_host"]
    protocol = legend_config["grafana_protocol"]
    grafana_url = urljoin("%s://%s" % (protocol, host), resp["url"])

    logger.debug(resp)

    return {
        "status": "Available",
        "uid": resp["uid"],
        "id": resp["id"],
        "grafana_url": grafana_url,
    }

@kopf.on.create("grofers.io", "v1beta1", "grafana-dashboards")
@kopf.on.resume("grofers.io", "v1beta1", "grafana-dashboards")
@kopf.on.update("grofers.io", "v1beta1", "grafana-dashboards")
def handler(spec, name, **kwargs):
    logger.debug("Event: %s",kwargs['event'])
    action=kwargs["event"]
    if action == 'create':
        logger.info("Creating new Grafana dashboard: %s", name)
        kopf.info(
            spec, reason="CreatingDashboard", message="Creating new grafana-dashboard."
        )
        logger.debug("Got the following keyword args for creating the object: %s", kwargs)
    else:
        logger.info("Updating existing Grafana dashboard object: %s", name)
        kopf.info(spec, reason="UpdatingDashboard", message="Updating Grafana dashboard.")
        logger.debug("Got the following keyword args for updating the object: %s", kwargs)
    
    try:
        resp = create_or_update_handler(spec, name, **kwargs)
        if action == 'create':
            kopf.info(
                spec,reason="CreatedDashboard",message=("Finished creating dashboard " "at %s." % resp["grafana_url"])
            )
            logger.info("Finished creating Grafana dashboard: %s", name)            
        else:
            kopf.info(
                spec,reason="UpdatedDashboard",message="Finished updating Grafana dashboard: %s." % name
            )
            logger.info("Finished updating Grafana dashboard: %s", name)
        return resp
        
    except Exception as e:
        logger.error(
            (
                "Failed to %s Grafana dashboard due to the "
                "following exception: %s"
            ),
            action,
            e,
        )
        kopf.exception(
            spec,
            reason="APIError",
            message=("Failed to %s dashboard due to API " "error: %s",action, e),
        )
        raise kopf.PermanentError("Failed creating the dashboard")


@kopf.on.delete("grofers.io", "v1beta1", "grafana-dashboards")
def delete_handler(spec, name, body, **kwargs):
    logger.info("Deleting Grafana dashboard: %s", name)
    kopf.info(spec, reason="DeletingDashboard", message="Deleting grafana dashboard.")
    logger.debug("Got the following keyword args for deleting the object: %s", kwargs)

    # Fetch the uid / try deleting the dashboard only if the object creation
    # was successful earlier
    if "status" in body:
        status = body["status"]
        if status.get("handler"):
            uid = body["status"]["handler"]["uid"]

            try:
                legend_config = load_legend_config()
                status = delete_dashboard(legend_config, uid)
                kopf.info(
                    spec,
                    reason="DeletedDashboard",
                    message="Finished deleting dashboard:  %s." % name,
                )
                logger.info("Finished deleting Grafana dashboard: %s", name)
                return {"status": status}
            except Exception as e:
                logger.error(
                    (
                        "Failed to delete dashboard due to the following "
                        "exception: %s"
                    ),
                    e,
                )
                kopf.exception(
                    spec,
                    reason="APIError",
                    message=("Failed to delete dashboard due to API " "error: %s" % e),
                )
                raise kopf.PermanentError("Failed deleting the dashboard")
    else:
        kopf.info(
            spec,
            reason="DeletedDashboard",
            message="Finished deleting dashboard:  %s." % name,
        )
        logger.info("Finished deleting Grafana dashboard: %s", name)
        return {"status": "Deleted"}

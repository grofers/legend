import logging
import os

import kopf

from urllib.parse import urljoin

from legend import legend


LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
DEV = os.environ.get('DEV', False)

logging.basicConfig(format='%(module)s [%(levelname)s] %(message)s',
                    level=getattr(logging, LOG_LEVEL))
logger = logging.getLogger(__name__)
logger.setLevel(getattr(logging, LOG_LEVEL))

GRAFANA_API_KEY = os.environ['GRAFANA_API_KEY']
GRAFANA_HOST = os.environ['GRAFANA_HOST']
GRAFANA_PROTOCOL = os.environ['GRAFANA_PROTOCOL']

logger.info(('Starting grafana-dashboards operator to create to manage '
             'Grafana dashboards at %s://%s.'), GRAFANA_PROTOCOL, GRAFANA_HOST)


if DEV:
    logger.info('Startin DEV mode')
    from dev import login_handler


def create_or_update_handler(spec, name, **kwargs):
    body = kwargs['body']
    spec = body['spec']
    id = None
    if 'status' in body:
        id = body['status']['create_handler']['id']

    resp = legend.create_or_update_dashboard(GRAFANA_API_KEY, GRAFANA_HOST,
                                             GRAFANA_PROTOCOL, spec, id)
    grafana_url = urljoin('%s://%s' % (GRAFANA_PROTOCOL, GRAFANA_HOST),
                          resp['url'])
    logger.debug(resp)

    return {
        'status': 'Available',
        'uid': resp['uid'],
        'id': resp['id'],
        'grafana_url': grafana_url,
    }


@kopf.on.create('grofers.io', 'v1', 'grafana-dashboards')
def create_handler(spec, name, **kwargs):
    logger.info('Creating new Grafana dashboard: %s', name)
    kopf.info(spec, reason='CreatingDashboard',
              message='Creating new grafana-dashboard.')
    logger.debug('Got the following keyword args for creaating the object: %s',
                 kwargs)

    try:
        resp = create_or_update_handler(spec, name, **kwargs)
        kopf.info(spec, reason='CreatedDashboard',
                  message=('Finished creating dashboard '
                           'at %s.' % resp['grafana_url']))
        logger.info('Finished creating Grafana dashboard: %s', name)
        return resp
    except Exception as e:
        logger.error(('Failed to create Grafana dashboard due to the '
                      'following exception: %s'), e)
        kopf.exception(spec, reason='APIError',
                       message=('Failed to create dashboard due to API '
                                'error: %s' % e))
        raise e


@kopf.on.update('grofers.io', 'v1', 'grafana-dashboards')
def update_handler(spec, name, **kwargs):
    logger.info('Updating existing Grafana dashboard object: %s', name)
    kopf.info(spec, reason='UpdatingDashboard',
              message='Updating Grafana dashboard.')
    logger.debug('Got the following keyword args for udpating the object: %s',
                 kwargs)

    try:
        create_or_update_handler(spec, name, **kwargs)
        kopf.info(spec, reason='UpdatedDashboard',
                  message='Finished updating Grafana dashboard: %s.' % name)
        logger.info('Finished updating Grafana dashboard: %s', name)
    except Exception as e:
        logger.error(('Failed to update Grafana dashboard due to the '
                      'following exception: %s'), e)
        kopf.exception(spec, reason='APIError',
                       message=('Failed to update dashboard due to API '
                                'error: %s' % e))
        raise e


@kopf.on.delete('grofers.io', 'v1', 'grafana-dashboards')
def delete_handler(spec, name, body, **kwargs):
    logger.info('Deleting Grafana dashboard: %s', name)
    kopf.info(spec, reason='DeletingDashboard',
              message='Deleting grafana dashboard.')
    logger.debug('Got the following keyword args for deleting the object: %s',
                 kwargs)
    uid = body['status']['create_handler']['uid']

    try:
        legend.delete_dashboard(GRAFANA_API_KEY, GRAFANA_HOST,
                                GRAFANA_PROTOCOL, uid)
        kopf.info(spec, reason='DeletedDashboard',
                  message='Finished deleting dashboard:  %s.' % name)
        logger.info('Finished deleting Grafana dashboard: %s', name)
        return {'status': 'Deleted'}
    except Exception as e:
        logger.error(('Failed to delete dashboard due to the following '
                      'exception: %s'), e)
        kopf.exception(spec, reason='APIError',
                       message=('Failed to delete dashboard due to API '
                                'error: %s' % e))
        raise e

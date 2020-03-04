pgsql_rds_schema = {
    'dimensions': {'type': 'list', 'schema': {'type': 'dict', 'schema': {
        'db_instance_identifier': {'type': 'string', 'required': True},
    }}}}

platform_k8s_deployment_schema = {
    'dimensions': {'type': 'list', 'schema': {'type': 'dict', 'schema': {
        'deployment_name': {'type': 'string', 'required': True},
    }}}}

mysql_56_rds_schema = {
    'dimensions': {'type': 'list', 'schema': {'type': 'dict', 'schema': {
        'db_instance_identifier': {'type': 'string', 'required': True},
    }}}}

sqs_schema = {
    'dimensions': {'type': 'list', 'schema': {'type': 'dict', 'schema': {
        'queue_name': {'type': 'string', 'required': True},
        'dead_queue_name': {'type': 'string', 'required': False},
    }}}}

springboot_schema = {
    'dimensions': {'type': 'list', 'schema': {'type': 'dict', 'schema': {
        'job': {'type': 'string', 'required': True},
    }}}}

rabbitmq_schema = {
    'dimensions': {'type': 'list', 'schema': {'type': 'dict', 'schema': {
        'queue_name': {'type': 'string', 'required': True},
        'job': {'type': 'string', 'required': True},
        'dead_queue_name': {'type': 'string', 'required': False, 'nullable': True},
    }}}}

jmx_schema = {
    'dimensions': {'type': 'list', 'schema': {'type': 'dict', 'schema': {
        'job': {'type': 'string', 'required': True},
    }}}}

haproxy_schema = {
    'dimensions': {'type': 'list', 'schema': {'type': 'dict', 'schema': {
        'backend': {'type': 'string', 'required': True},
    }}}}

elb_schema = {
    'dimensions': {'type': 'list', 'schema': {'type': 'dict', 'schema': {
        'load_balancer_name': {'type': 'string', 'required': True},
    }}}}

django_schema = {
    'dimensions': {'type': 'list', 'schema': {'type': 'dict', 'schema': {
        'job': {'type': 'string', 'required': True},
    }}}}

couchdb_schema = {
    'dimensions': {'type': 'list', 'schema': {'type': 'dict', 'schema': {
        'job_name': {'type': 'string', 'required': True},
    }}}}

consul_schema = {
    'dimensions': {'type': 'list', 'schema': {'type': 'dict', 'schema': {
        'region': {'type': 'string', 'required': True},
    }}}}

promtail_schema = {
    'dimensions': {'type': 'list', 'schema': {'type': 'dict', 'schema': {
        # Desc about the metric
        'pod_name': {'type': 'string', 'required': True},
    }}}}

celery_schema = {
    'dimensions': {'type': 'list', 'schema': {'type': 'dict', 'schema': {
        'job_name': {'type': 'string', 'required': True},
    }}}}

redis_schema = {
    'dimensions': {'type': 'list', 'schema': {'type': 'dict', 'schema': {
        'job_name': {'type': 'string', 'required': True},
    }}}}

systemcore_ec2_schema = {
    'dimensions': {'type': 'list', 'schema': {'type': 'dict', 'schema': {
        'host': {'type': 'string', 'required': True},
    }}}}

s3_schema = {
    'dimensions': {'type': 'list', 'schema': {'type': 'dict', 'schema': {
        'bucket_name': {'type': 'string', 'required': True},
        'filter_id': {'type': 'string', 'required': True}
    }}}}

mysql_ec2_schema = {
    'dimensions': {'type': 'dict', 'schema': {
        'ec2': {'required': True, 'type': 'list', 'schema': {'type': 'dict', 'schema': {'host': {'type': 'string', 'required': True}}}},
        'db': {'required': True, 'type': 'list', 'schema': {'type': 'dict', 
                'schema': {
                    'masters': {'required': False, 'type': 'list', 'schema': {'type': 'dict',
                                'schema': {'host': {'type': 'string', 'required': True},
                                           'db_name': {'type': 'string', 'required': True}}}},
                    'slaves': {'required': False, 'type': 'list', 'schema': {'type': 'dict',
                               'schema': {'host': {'type': 'string', 'required': True},
                                          'db_name': {'type': 'string', 'required': True}}}}
    }}}}}
}

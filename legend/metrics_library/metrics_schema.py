from typing_extensions import Required


airflow_schema = {
    "data_source": {"type": "string", "required": False},
    "dimensions": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "cluster": {"type": "string", "required": True},
                "namespace": {"type": "string", "required": True},
                "dag_id": {"type": "string", "required": True},
            },
        },
    },
}

starlette_schema = {
    "data_source": {"type": "string", "required": False},
    "dimensions": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "job": {"type": "string", "required": True},
                "path": {"type": "string", "required": True},
            },
        },
    },
}

pgsql_rds_schema = {
    "data_source": {"type": "string", "required": False},
    "dimensions": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "db_instance_identifier": {"type": "string", "required": True},
                "region": {"type": "string", "required": False},
                "is_replica": {"type": "boolean", "required": False},
                "is_aurora": {"type": "boolean", "required": False},
                "is_disk_gp2": {"type": "boolean", "required": False},
                "is_burst_balance_panel_required": {
                    "type": "boolean",
                    "required": False,
                },
            },
        },
    },
}

pgbouncer_schema = {
    "data_source": {"type": "string", "required": False},
    "dimensions": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {"job_name": {"type": "string", "required": True},},
        },
    },
}

platform_k8s_deployment_schema = {
    "data_source": {"type": "string", "required": False},
    "dimensions": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {"deployment_name": {"type": "string", "required": True},},
        },
    },
}

platform_k8s_statefulset_schema = {
    "data_source": {"type": "string", "required": False},
    "dimensions": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {"statefulset_name": {"type": "string", "required": True},},
        },
    },
}

platform_k8s_cronjob_schema = {
    "data_source": {"type": "string", "required": False},
    "dimensions": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "namespace": {"type": "string", "required": True},
                "cronjob_name": {"type": "string", "required": True},
            },
        },
    },
}

platform_k8s_hpa_schema = {
    "data_source": {"type": "string", "required": False},
    "dimensions": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "deployment_name": {"type": "string", "required": True},
                "hpa_name": {"type": "string", "required": True},
            },
        },
    },
}

platform_k8s_ingress_schema = {
    "data_source": {"type": "string", "required": False},
    "dimensions": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "namespace": {"type": "string", "required": True},
                "service_name": {"type": "string", "required": True},
                "service_type": {"type": "string", "required": True},
            },
        },
    },
}

mysql_56_rds_schema = {
    "data_source": {"type": "string", "required": False},
    "dimensions": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "db_instance_identifier": {"type": "string", "required": True},
                "region": {"type": "string", "required": False},
                "is_replica": {"type": "boolean", "required": False},
                "is_aurora": {"type": "boolean", "required": False},
                "is_disk_gp2": {"type": "boolean", "required": False},
                "is_burst_balance_panel_required": {
                    "type": "boolean",
                    "required": False,
                },
            },
        },
    },
}

sqs_schema = {
    "data_source": {"type": "string", "required": False},
    "dimensions": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "queue_name": {"type": "string", "required": True},
                "dead_queue_name": {"type": "string", "required": False},
            },
        },
    },
}

springboot_schema = {
    "data_source": {"type": "string", "required": False},
    "dimensions": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {"job": {"type": "string", "required": True},},
        },
    },
}

rabbitmq_schema = {
    "data_source": {"type": "string", "required": False},
    "dimensions": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "queue_name": {"type": "string", "required": True},
                "job": {"type": "string", "required": True},
                "dead_queue_name": {
                    "type": "string",
                    "required": False,
                    "nullable": True,
                },
            },
        },
    },
}

jmx_schema = {
    "data_source": {"type": "string", "required": False},
    "dimensions": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "job": {"type": "string", "required": True},
                "service": {"type": "string", "required": False},
            },
        },
    },
}

haproxy_schema = {
    "data_source": {"type": "string", "required": False},
    "dimensions": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {"backend": {"type": "string", "required": True},},
        },
    },
}

elb_schema = {
    "data_source": {"type": "string", "required": False},
    "dimensions": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {"load_balancer_name": {"type": "string", "required": True},},
        },
    },
}

alb_schema = {
    "data_source": {"type": "string", "required": False},
    "dimensions": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "load_balancer_id": {"type": "string", "required": True},
                "target_group_id": {"type": "string", "required": True},
                "region": {"type": "string", "required": False},
            },
        },
    },
}

django_schema = {
    "data_source": {"type": "string", "required": False},
    "dimensions": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {"job": {"type": "string", "required": True},},
        },
    },
}

flask_schema = {
    "data_source": {"type": "string", "required": False},
    "dimensions": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {"job": {"type": "string", "required": True},},
        },
    },
}

playframework_schema = {
    "data_source": {"type": "string", "required": False},
    "dimensions": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {"service": {"type": "string", "required": True},},
        },
    },
}

couchdb_schema = {
    "data_source": {"type": "string", "required": False},
    "dimensions": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {"job_name": {"type": "string", "required": True},},
        },
    },
}

consul_schema = {
    "data_source": {"type": "string", "required": False},
    "dimensions": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {"region": {"type": "string", "required": True},},
        },
    },
}

vault_schema = {
    "data_source": {"type": "string", "required": False},
    "dimensions": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {"environment": {"type": "string", "required": True},},
        },
    },
}

promtail_schema = {
    "data_source": {"type": "string", "required": False},
    "dimensions": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                # Desc about the metric
                "pod_name": {"type": "string", "required": True},
            },
        },
    },
}

celery_schema = {
    "data_source": {"type": "string", "required": False},
    "dimensions": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {"job_name": {"type": "string", "required": True},},
        },
    },
}

redis_schema = {
    "data_source": {"type": "string", "required": False},
    "dimensions": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {"job_name": {"type": "string", "required": True},},
        },
    },
}

redis_elasticache_schema = {
    "data_source": {"type": "string", "required": False},
    "dimensions": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "cache_cluster_identifier": {"type": "string", "required": True},
                "region": {"type": "string", "required": False},
                "is_redis_version_below_three": {"type": "boolean", "required": False} 
            },
        },
    },
}

platform_ec2_schema = {
    "data_source": {"type": "string", "required": False},
    "dimensions": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {"host": {"type": "string", "required": True},},
        },
    },
}

slo_schema = {
    "data_source": {"type": "string", "required": False},
    "dimensions": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "name": {"type": "string", "required": True},
                "availablity": {"type": "string", "required": True},
                "totalQuery": {"type": "string", "required": True},
                "errorQuery": {"type": "string", "required": True},
            },
        },
    },
}


s3_schema = {
    "data_source": {"type": "string", "required": False},
    "dimensions": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "bucket_name": {"type": "string", "required": True},
                "filter_id": {"type": "string", "required": True},
            },
        },
    },
}

mysql_ec2_schema = {
    "data_source": {"type": "string", "required": False},
    "dimensions": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "masters": {
                    "required": True,
                    "type": "list",
                    "schema": {
                        "type": "dict",
                        "schema": {
                            "host": {"type": "string", "required": True},
                            "db_name": {"type": "string", "required": True},
                        },
                    },
                },
                "slaves": {
                    "required": False,
                    "type": "list",
                    "schema": {
                        "type": "dict",
                        "schema": {
                            "host": {"type": "string", "required": True},
                            "db_name": {"type": "string", "required": True},
                        },
                    },
                },
            },
        },
    },
}

nodejs_schema = {
    "data_source": {"type": "string", "required": False},
    "dimensions": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {"job": {"type": "string", "required": True},},
        },
    },
}

go_schema = {
    "data_source": {"type": "string", "required": False},
    "dimensions": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {"job": {"type": "string", "required": True},},
        },
    },
}

loki_schema = {
    "data_source": {"type": "string", "required": False},
    "dimensions": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "labels": {
                    "type": "dict",
                    "required": True,
                    "allow_unknown": True,
                    "schema": {"namespace": {"type": "string", "required": True,}},
                },
                "filters": {"type": "list", "required": False,},
            },
        },
    },
}

nginx_schema = {
    "data_source": {"type": "string", "required": False},
    "dimensions": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {"nginx_namespace": {"type": "string", "required": True},},
        },
    },
}

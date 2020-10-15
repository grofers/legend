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
            },
        },
    },
}

platform_k8s_deployment_schema = {
    "data_source": {"type": "string", "required": False},
    "dimensions": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "deployment_name": {"type": "string", "required": True},
            },
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
            "schema": {
                "job": {"type": "string", "required": True},
            },
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
            "schema": {
                "backend": {"type": "string", "required": True},
            },
        },
    },
}

elb_schema = {
    "data_source": {"type": "string", "required": False},
    "dimensions": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "load_balancer_name": {"type": "string", "required": True},
            },
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
            "schema": {
                "job": {"type": "string", "required": True},
            },
        },
    },
}

playframework_schema = {
    "data_source": {"type": "string", "required": False},
    "dimensions": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "service": {"type": "string", "required": True},
            },
        },
    },
}

couchdb_schema = {
    "data_source": {"type": "string", "required": False},
    "dimensions": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "job_name": {"type": "string", "required": True},
            },
        },
    },
}

consul_schema = {
    "data_source": {"type": "string", "required": False},
    "dimensions": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "region": {"type": "string", "required": True},
            },
        },
    },
}

vault_schema = {
    "data_source": {"type": "string", "required": False},
    "dimensions": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "environment": {"type": "string", "required": True},
            },
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
            "schema": {
                "job_name": {"type": "string", "required": True},
            },
        },
    },
}

redis_schema = {
    "data_source": {"type": "string", "required": False},
    "dimensions": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "job_name": {"type": "string", "required": True},
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
            "schema": {
                "host": {"type": "string", "required": True},
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
        "type": "dict",
        "schema": {
            "ec2": {
                "required": True,
                "type": "list",
                "schema": {
                    "type": "dict",
                    "schema": {"host": {"type": "string", "required": True}},
                },
            },
            "db": {
                "required": True,
                "type": "list",
                "schema": {
                    "type": "dict",
                    "schema": {
                        "masters": {
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
        },
    },
}

nodejs_schema = {
    "data_source": {"type": "string", "required": False},
    "dimensions": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "job": {"type": "string", "required": True},
            },
        },
    },
}

go_schema = {
    "data_source": {"type": "string", "required": False},
    "dimensions": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "job": {"type": "string", "required": True},
            },
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
                    "schema": {
                        "namespace": {
                            "type": "string",
                            "required": True,
                        }
                    },
                },
                "filters": {
                    "type": "list",
                    "required": False,
                },
            },
        },
    },
}

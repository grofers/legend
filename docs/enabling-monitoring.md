
# Client Libraries & Integration Guides

> This guide is only about enabling the metrics in the respective components, but doesn't not guide on enabling scrapping of the merics where applicable (ex: prometheus). Internally we user promethues operator and service monitor concept - [https://github.com/prometheus-operator/prometheus-operator/blob/master/Documentation/user-guides/getting-started.md](https://github.com/prometheus-operator/prometheus-operator/blob/master/Documentation/user-guides/getting-started.md )

## Table of contents

* [Django](#django)
* [Celery](#celery)
* [MySql EC2](#mysql-ec2)
* [Redis](#redis)
* [Rabbitmq](#rabbitmq)
* [Couchdb](#couchdb)
* [Nodejs](#nodejs)
* [Golang](#golang)
* [PgBouncer](#PgBouncer)
* [Nginx](#Nginx)
## Django

### Configure prometheus metrics exporter

You can set up  [django-prometheus](https://github.com/korfuri/django-prometheus)  exporter for your service by referring to the README here:  [https://github.com/grofers/django-prometheus/tree/v1.0.16](https://github.com/grofers/django-prometheus/tree/v1.0.16). This is specific becuase of the frozen django version. If your service supports you can probably user the upstream exporter itself

### Enable metrics django framweok

Please follow  [django-prometheus](https://pypi.org/project/django-prometheus/)

### Enable Nginx Monitoring

Prometheus will try to fetch `/metrics` and scrape all the open HTTP ports of instances tagged in the manifest causing that the Prometheus scraper throws 404 when trying to scrape HTTP servers that don’t expose metrics. This happens because all the endpoints mentioned urls.py are restricted to avoid being public. We can enable /metrics in nginx config such that prometheus is able to scrape this.
Reference -
 [https://www.linode.com/docs/web-servers/nginx/how-to-configure-nginx/#location-blocks](https://www.linode.com/docs/web-servers/nginx/how-to-configure-nginx/#location-blocks)  

## Celery

[celery-prometheus-exporter](https://github.com/zerok/celery-prometheus-exporter)  is an exporter for Celery related metrics in order to get picked up by Prometheus.
You can set up celery-prometheus-exporter for your service by referring the below link  [https://github.com/zerok/celery-prometheus-exporter](https://github.com/zerok/celery-prometheus-exporter)  

### Example

This is a sample deployment following the documenatation to setup metrics over the celery queue using redis

```yaml
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: celery-prometheus-exporter
  namespace: sample-ns
  labels:
    app: sample-app
    service: sample-service
spec:
  selector:
    matchLabels:
      app: sample-app
  template:
    metadata:
      name: sample-app
      labels:
        app: sample-app
        service: sammple-service
    spec:
      containers:
      - image: zerok/celery-prometheus-exporter:1.7.0-celery4
        name: celery-prometheus-exporter
        args:
        - "--enable-events"
        imagePullPolicy: Always
        env:
        - name: BROKER_URL
          value: 'redis://172.31.107.38:6379/3'
```

## MySql EC2

To consume the metrics from MySQL we should setup PMM server on each MySQL instance. Once the servers are exposing metrics, we should enable scarping to insert into prometheus. One way to do it is create a static kubernetes `endpoint` pointing to the instance and further creating a `service` pointing to this `endpoint` and having a `service monitor` scarpping

```yaml
---
apiVersion: v1
kind: Endpoints
metadata:
  name: sample-mysql
  namespace: sample-ns
  labels:
    app: sample-app
subsets:
- addresses:
  - ip: 1.2.3.4

  ports:
  - name: metrics
    port: 42002
    protocol: TCP
  - name: system-metrics
    port: 42000
    protocol: TCP

---

apiVersion: v1
kind: Service
metadata:
  name: sample-service
  namespace: sample-ns
  labels:
    app: sample-app
spec:
  type: ClusterIP
  ports:
  - name: metrics
    protocol: TCP
    port: 42002
    targetPort: 42002
  - name: system-metrics
    protocol: TCP
    port: 42000
    targetPort: 42000

---

apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: sample-app-sm
  namespace: sample-ns
  labels:
    app: sample-app
    release: prom-op
spec:
  selector:
    matchLabels:
      app: sample-app
    namespaceSelector:
      matchNames:
      - sample-ns
  endpoints:
  - port: system-metrics
    tlsConfig:
      insecureSkipVerify: true
    scheme: https
    interval: 10s
    honorLabels: true
    basicAuth:
      password:
        name: percona-mysql-metrics-cred
        key: password
      username:
        name: percona-mysql-metrics-cred
        key: user

  - port: metrics
    tlsConfig:
      insecureSkipVerify: true
    path: /metrics-hr
    scheme: https
    interval: 10s
    honorLabels: true
    basicAuth:
      password:
        name: percona-mysql-metrics-cred
        key: password
      username:
        name: percona-mysql-metrics-cred
        key: user
```

## Redis

Exporter - oliver006/redis_exporter:v1.3.5-alpine to expose metrics from Redis EC2.

```yaml
---

apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis-prometheus-exporter
  namespace: sample-ns
  labels:
    app: sample-app
    service: sample-service
spec:
  selector:
    matchLabels:
      app: sample-app
  template:
    metadata:
      name: redis-prometheus-exporter
      labels:
        app: sample-app
        service: sample-service
    spec:
      containers:
      - image: oliver006/redis_exporter:v1.3.5-alpine
        name: redis-prometheus-exporter
        imagePullPolicy: Always
        env:
        - name: REDIS_ADDR
          value: 'redis://172.31.107.38:6379'
        - name: REDIS_EXPORTER_CHECK_KEYS
          value: 'db0=*'
        - name: REDIS_EXPORTER_INCL_SYSTEM_METRICS
          value: 'true'
```

## RabbitMQ

Check for your RabbitMQ version with the following command. Look for `{rabbit,”RabbitMQ”,”3.6.15”}`

```shell
sudo rabbitmqctl status
```

*For RabbitMQ versions:*
*`3.6.x` and `3.7.x`
Exporter - [https://github.com/deadtrickster/prometheus_rabbitmq_exporter](https://github.com/deadtrickster/prometheus_rabbitmq_exporter) to expose metrics to prometheus.

Depending on the version of RabbitMQ you need to download relevant release , which you will have to enable on your machine where your RabbitMQ is running.

Go to the section Install the rabbitmq prometheus exporter in this link. [http://www.hontecillas.com/setup_prometheus_and_grafana.html](http://www.hontecillas.com/setup_prometheus_and_grafana.html). Download the relevant release in the path where other rabbitmq plugins are installed , mostly it will be `/usr/lib/rabbitmq/lib/rabbitmq-server-[version]/plugins` or `/usr/lib/rabbitmq/plugins`

Do not download  [prometheus_process_collector-1.3.0.FreeBSD.ez](https://github.com/deadtrickster/prometheus_rabbitmq_exporter/releases/download/rabbitmq-3.6.14.1/prometheus_process_collector-1.3.0.FreeBSD.ez)  otherwise might face loading errors while enabling plugins after downloading just enable the plugin

*`3.8.x`
Use  [https://github.com/rabbitmq/rabbitmq-prometheus](https://github.com/rabbitmq/rabbitmq-prometheus)  
For versions above 3.8.x rabbitmq-prometheus plugin comes shipped with the rabbitmq distribution so you will just need to enable the plugin and it will start exposing its metrics.

For k8s service file

```yaml
---
apiVersion: v1
kind: Endpoints
metadata:
  name: service-rabbitmq-metrics
  namespace: samepl-ns
  labels:
    app: sample-app
subsets:
  - addresses:
      - ip: 1.2.3.4
    ports:
      - name: metrics
        port: 15672
        protocol: TCP
---
apiVersion: v1
kind: Service
metadata:
  name: service-rabbitmq-metrics
  namespace: sample-ns
  labels:
    app: sample-app
spec:
  type: ClusterIP
  ports:
    - name: metrics
      protocol: TCP
      port: 80
      targetPort: 80
```

To get queue based metrics, enable per object metric collection using the prometheus.return_per_object_metrics = true, in the rabbitmq.conf. More info here at  [Per Object Metrics](https://www.rabbitmq.com/prometheus.html#metric-aggregation) (This has a performance impact, so please read the docs for that).

_Note:_ If using legend to configure RabbitMQ monitoring, remember to enable prometheus return_per_object_metrics, else most graphs won’t show any data

# Couchdb

Exporter - [gesellix/couchdb-prometheus-exporter](https://github.com/gesellix/couchdb-prometheus-exporter) to expose metrics from couchdb ec2 instances.

# Nodejs

Please setup prom-client exporter for your nodejs application
Install from:  [https://github.com/siimon/prom-client](https://github.com/siimon/prom-client)  
To override default buckets, please keep metric_name as `http_request_duration_in_seconds`, as we are querying using this metric_name `http_request_duration_in_seconds` in legend.

```shell
const httpRequestDurationInSeconds = new Prometheus.Histogram({
  name: ‘http_request_duration_in_seconds’,
  help: ‘Duration of HTTP requests in seconds’,
  labelNames: [‘method’, ‘route’, ‘code’],
  buckets: [0.001, 0.01, 0.1, 1, 2, 3, 4, 5, 10, 20] // buckets for response time from 0.001seconds to 20seconds
});
```

# Golang

Please setup client_golang exporter for your GO application
Install from: [https://github.com/prometheus/client_golang](https://github.com/prometheus/client_golang)

# PgBouncer

Please setup PgBouncer exporter from [here](https://github.com/spreaker/prometheus-pgbouncer-exporter).

# NGINX

* Please setup the Prometheus-NginxLog-Exporter from [here](https://github.com/martin-helmich/prometheus-nginxlog-exporter).
* Please setup namespacing over your NGINX (don't mistake this for kubernetes namespace. They are not at all related ). Refer to [this](https://github.com/martin-helmich/prometheus-nginxlog-exporter#namespace-as-labels) for more details around nginx namespacing. 
  * Do not use any other special characters apart from "underscores" (_) while naming any namespace as the namespace names are used directly as placeholders in the names of the metrics created by the above exporter (for example `<namespace>_http_response_count_total`) and prometheus would expect all the metric names to NOT contain any special character apart from underscores (\_).
* Finally, setup a Prometheus server to periodically scrape the `/metrics` endpoint exposed by the above prometheus-nginxlog-exporter thereby, exposing the required NGINX metrics. 
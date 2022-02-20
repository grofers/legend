# Contributing to kubernetes library

> The default kubernetes objects which are created with required metric components

## Overview

Legend supports a wide variety of metric types for creating panels for "components" like SQS, Promtail, Loki, EC2 and many more. Refer to [sample_input.yaml](../sample_input.yaml) for getting to know all the supported metrics.

But if your use-case requires certain kubernetes objects to be created before legend plots panels you can extend your metric component by adding to kubernetes library.

## Implementation

Legend relys heavily on templating and name-schema. So to add a component to kubernetes library in parity to the component which is added in metric library you'll just need to create a python file with same name on path `legend/kubernetes_library` and implement `run` function with your business logic.

Example:
* You have added a new metric component to metric library: `kryptonite`
* Following component needs a pod to be deployed on kubernetes cluster before legend plots a panel.
* Just add `kryptonite.py` on path `legend/kubernetes_library` and implement `run`.

Sample Kubernetes Component
* Metric component named `slo`: [slo_metrics.j2](../legend/metrics_library/metrics/slo_metrics.j2)
* Kubernetes Library Implementation for `slo`: [slo.py](../legend/kubernetes_library/slo.py)



# Legend Internals

## How does legend work internally

* Legend makes use of [grafonnet-lib](https://github.com/grafana/grafonnet-lib).
* With grafonnet-lib, legend builds relevant dashboard files declaratively in [jsonnet](https://jsonnet.org/) format based on the provided input YAML manifest.
* And, it finally makes use of Grafana API to push those corresponding dashboards to the respective grafana endpoint (provided by the user in legend's initial configuration).

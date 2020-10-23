# Installing Legend Using Helm v3
* Please setup helm v3 on your system. Refer to [helm's docs](https://helm.sh/docs/).
* Please edit the [values.yaml](./values.yaml) according to your use-case's configuration. 
* Run the following command:
```sh
helm install <legend-release-name> ./legend -f values.yaml
```

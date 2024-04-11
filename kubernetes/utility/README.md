## main

utility is my cluster for core components.

## How to bootstrap

Assuming you are in the `utility` root folder:

### Flux

#### Install Flux

```sh
kubectl apply --server-side --kustomize ./bootstrap
```

### Apply Cluster Configuration

_These cannot be applied with `kubectl` in the regular fashion due to some files being encrypted with sops_

```sh
sops --decrypt ./flux/vars/cluster-secrets.sops.yaml | kubectl apply -f -
kubectl apply -f ./flux/vars/cluster-settings.yaml
```

### Kick off Flux applying this repository

```sh
kubectl apply --server-side --kustomize ./flux/config
```

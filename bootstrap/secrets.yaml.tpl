---
apiVersion: v1
kind: Namespace
metadata:
  name: external-secrets
---
apiVersion: v1
kind: Secret
metadata:
  name: onepassword-secret
  namespace: external-secrets
stringData:
  1password-credentials.json: op://Kubernetes/1password/OP_CREDENTIALS_JSON
  token: op://Kubernetes/1password/OP_CONNECT_TOKEN
---
apiVersion: v1
kind: Namespace
metadata:
  name: flux-system
---
apiVersion: v1
kind: Secret
metadata:
  name: sops-age-secret
  namespace: flux-system
stringData:
  age.agekey: op://Kubernetes/sops/SOPS_PRIVATE_KEY
---
apiVersion: v1
kind: Secret
metadata:
  name: cluster-secrets
  namespace: flux-system
stringData:
  SECRET_DOMAIN: op://Kubernetes/domains/DOMAIN
  SECRET_DOMAIN_INT: op://Kubernetes/domains/DOMAIN_INT
  SECRET_DOMAIN_INTERNAL: op://Kubernetes/domains/DOMAIN_INTERNAL
  SECRET_DOMAIN_SHORT: op://Kubernetes/domains/DOMAIN_SHORT

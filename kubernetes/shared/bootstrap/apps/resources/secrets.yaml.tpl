---
apiVersion: v1
kind: Namespace
metadata:
  name: security
---
apiVersion: v1
kind: Secret
metadata:
  name: onepassword-secret
  namespace: security
stringData:
  1password-credentials.json: op://$VAULT/1password/OP_CREDENTIALS_JSON
  token: op://$VAULT/1password/OP_CONNECT_TOKEN
---
apiVersion: v1
kind: Namespace
metadata:
  name: flux-system
---
apiVersion: v1
kind: Secret
metadata:
  name: sops-age
  namespace: flux-system
stringData:
  age.agekey: op://kubernetes/sops/SOPS_PRIVATE_KEY
---
apiVersion: v1
kind: Secret
metadata:
  name: cluster-secrets
  namespace: flux-system
stringData:
  SECRET_DOMAIN: op://$VAULT/domains/DOMAIN
  SECRET_DOMAIN_INT: op://$VAULT/domains/DOMAIN_INT
  SECRET_DOMAIN_INTERNAL: op://$VAULT/domains/DOMAIN_INTERNAL
  SECRET_DOMAIN_SHORT: op://$VAULT/domains/DOMAIN_SHORT

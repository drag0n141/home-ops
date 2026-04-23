resource "onepassword_item" "garage_k8s" {
  vault    = data.onepassword_vault.kubernetes.uuid
  title    = "garage-k8s"
  category = "password"

  section {
    label = "Admin"
    field {
      label = "ADMIN_AWS_ACCESS_KEY_ID"
      type  = "STRING"
      value = garage_key.admin_key.access_key_id
    }
    field {
      label = "ADMIN_AWS_SECRET_ACCESS_KEY"
      type  = "CONCEALED"
      value = garage_key.admin_key.secret_access_key
    }
  }

  dynamic "section" {
    for_each = toset(local.buckets)
    content {
      label = title(section.key)
      field {
        label = "${upper(section.key)}_AWS_ACCESS_KEY_ID"
        type  = "STRING"
        value = module.buckets[section.key].access_key_id
      }
      field {
        label = "${upper(section.key)}_AWS_SECRET_ACCESS_KEY"
        type  = "CONCEALED"
        value = module.buckets[section.key].access_key_secret
      }
    }
  }
}

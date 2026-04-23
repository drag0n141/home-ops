resource "onepassword_item" "garage_nas" {
  vault    = data.onepassword_vault.kubernetes.uuid
  title    = "garage-nas"
  category = "login"

  dynamic "section" {
    for_each = toset(local.buckets)
    content {
      label = section.key
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

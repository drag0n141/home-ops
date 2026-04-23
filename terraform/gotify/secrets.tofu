resource "onepassword_item" "gotify" {
  vault    = data.onepassword_vault.kubernetes.uuid
  title    = "gotify"
  category = "password"

  dynamic "section" {
    for_each = { for app in local.applications : app.name => app }
    content {
      label = section.key
      field {
        label = "GOTIFY_TOKEN_${upper(replace(replace(section.key, "-", "_"), " ", "_"))}"
        type  = "CONCEALED"
        value = gotify_application.app[section.key].token
      }
    }
  }
}

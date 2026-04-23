resource "onepassword_item" "gotify" {
  vault    = data.onepassword_vault.kubernetes.uuid
  title    = "gotify"
  category = "password"

  section {
    label = "Credentials"
    field {
      label = "GOTIFY_DEFAULTUSER_NAME"
      type  = "STRING"
      value = module.onepassword_gotify.fields["GOTIFY_DEFAULTUSER_NAME"]
    }
    field {
      label = "GOTIFY_DEFAULTUSER_PASS"
      type  = "CONCEALED"
      value = module.onepassword_gotify.fields["GOTIFY_DEFAULTUSER_PASS"]
    }
  }

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

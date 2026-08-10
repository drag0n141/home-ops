locals {
  applications = [
    { name = "Change-Detection" },
    { name = "CheckMK" },
    { name = "CVE-Report" },
    { name = "DB-Backup" },
    { name = "Fail2Ban" },
    { name = "Gatus" },
    { name = "Lidarr" },
    { name = "Prowlarr" },
    { name = "Proxmox" },
    { name = "Radarr" },
    { name = "Radarr4K" },
    { name = "Restic" },
    { name = "RSS-Forwarder" },
    { name = "SABnzbd" },
    { name = "Sonarr" },
    { name = "SonarrKids" },
    { name = "Sonarr4K" },
    { name = "Streamlink" },
    { name = "Uptime-Kuma" },
    { name = "USV" },
    { name = "YT-DLP" },
    { name = "Zerobyte" },
  ]
}

resource "gotify_application" "app" {
  for_each    = { for app in local.applications : app.name => app }
  name        = each.key
  description = each.key
}

# Gotify 3.0.0 stopped returning application tokens on GET; tokens are only
# exposed on creation or rotation (PUT /application/{id}/security). The
# gotify provider (0.3.0) still reads the token via GET on every refresh,
# so gotify_application.app[*].token gets wiped to "" before each plan/apply.
#
# Cache the token once here, right after it's set at creation time, and
# ignore all later changes so a refresh can't clobber the cached value.
# secrets.tofu reads the token from this cache instead of directly from
# gotify_application.
#
# var.app_token_overrides lets a token recovered outside of Terraform (e.g.
# regenerated in the Gotify UI and re-entered in 1Password) be seeded into
# the cache once, via the terraform-secret Secret + varsFrom - no local
# tofu run needed. Once the cache holds a real value, ignore_changes keeps
# it, so the override key can be cleared from the Secret again afterwards.
resource "terraform_data" "app_token_cache" {
  for_each = gotify_application.app

  input = coalesce(
    lookup(var.app_token_overrides, each.key, null),
    each.value.token,
  )

  lifecycle {
    ignore_changes = [input]
  }
}

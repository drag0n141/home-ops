locals {
  applications = [
    { name = "Change-Detection" },
    { name = "CheckMK" },
    { name = "CVE-Report" },
    { name = "DB-Backup" },
    { name = "Fail2Ban" },
    { name = "Gatus" },
    { name = "Lidarr" },
    { name = "Mind" },
    { name = "Prowlarr" },
    { name = "Proxmox" },
    { name = "Radarr" },
    { name = "Radarr4K" },
    { name = "Restic" },
    { name = "RSS-Forwarder" },
    { name = "SABnzbd" },
    { name = "Sonarr" },
    { name = "SonarrAnime" },
    { name = "SonarrDoVi" },
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

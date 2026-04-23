locals {
  applications = [
    { name = "Borg" },
    { name = "Change-Detection" },
    { name = "CheckMK" },
    { name = "Container-Monitoring" },
    { name = "CVE-Report" },
    { name = "DB-Backup" },
    { name = "Fail2Ban" },
    { name = "FTPGrab" },
    { name = "Gatus" },
    { name = "Home Assistant" },
    { name = "Jellyseerr" },
    { name = "Lidarr" },
    { name = "Mind" },
    { name = "Mount" },
    { name = "Overseerr" },
    { name = "pfSense" },
    { name = "Prowlarr" },
    { name = "Proxmox" },
    { name = "Pulse" },
    { name = "Radarr" },
    { name = "Radarr4K" },
    { name = "Rclone" },
    { name = "Readarr" },
    { name = "Restic" },
    { name = "RSS-Forwarder" },
    { name = "SABnzbd" },
    { name = "Sonarr" },
    { name = "SonarrAnime" },
    { name = "SonarrDoVi" },
    { name = "SonarrKids" },
    { name = "Sonarr4K" },
    { name = "StatusGator" },
    { name = "Streamlink" },
    { name = "Tautulli" },
    { name = "unRAID" },
    { name = "Uploader" },
    { name = "Uptime Kuma" },
    { name = "USV" },
    { name = "Whisparr" },
    { name = "YT-DLP" },
    { name = "Zerobyte" },
  ]
}

resource "gotify_application" "app" {
  for_each    = { for app in local.applications : app.name => app }
  name        = each.key
  description = each.key
}

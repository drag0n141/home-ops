#!/usr/bin/env python3
"""
Zerobyte Prometheus Exporter
Exports backup, repository and volume metrics from Zerobyte for Prometheus/VictoriaMetrics.
"""

import os
import time
import logging
import requests
from prometheus_client import start_http_server, Gauge, REGISTRY, PROCESS_COLLECTOR, PLATFORM_COLLECTOR

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("zerobyte-exporter")

# ── Configuration via environment variables ─────────────────────────────────────
ZEROBYTE_URL      = os.getenv("ZEROBYTE_URL", "http://localhost:4096")
ZEROBYTE_USERNAME = os.getenv("ZEROBYTE_USERNAME", "")
ZEROBYTE_PASS     = os.getenv("ZEROBYTE_PASSWORD", "")
SCRAPE_INTERVAL   = int(os.getenv("SCRAPE_INTERVAL", "60"))
EXPORTER_PORT     = int(os.getenv("EXPORTER_PORT", "9876"))

# ── Prometheus metrics ──────────────────────────────────────────────────────────

# Backups
backup_last_status = Gauge(
    "zerobyte_backup_last_status",
    "Last backup status (1=success, 0=error, 2=warning, 3=in_progress, -1=unknown)",
    ["schedule_name", "schedule_id", "volume_name", "repository_name"],
)
backup_last_at = Gauge(
    "zerobyte_backup_last_timestamp_seconds",
    "Unix timestamp of the last backup",
    ["schedule_name", "schedule_id", "volume_name", "repository_name"],
)
backup_next_at = Gauge(
    "zerobyte_backup_next_timestamp_seconds",
    "Unix timestamp of the next scheduled backup",
    ["schedule_name", "schedule_id", "volume_name", "repository_name"],
)
backup_enabled = Gauge(
    "zerobyte_backup_enabled",
    "Whether the backup schedule is enabled (1=yes, 0=no)",
    ["schedule_name", "schedule_id", "volume_name", "repository_name"],
)

# Repositories
repo_status = Gauge(
    "zerobyte_repository_status",
    "Repository status (1=healthy, 0=error, 2=unknown, -1=other)",
    ["repo_name", "repo_id", "repo_type"],
)
repo_last_checked = Gauge(
    "zerobyte_repository_last_checked_timestamp_seconds",
    "Unix timestamp of the last repository health check",
    ["repo_name", "repo_id", "repo_type"],
)
repo_total_size = Gauge(
    "zerobyte_repository_total_size_bytes",
    "Total size of the repository in bytes",
    ["repo_name", "repo_id"],
)
repo_snapshots_count = Gauge(
    "zerobyte_repository_snapshots_total",
    "Total number of snapshots in the repository",
    ["repo_name", "repo_id"],
)
repo_compression_ratio = Gauge(
    "zerobyte_repository_compression_ratio",
    "Compression ratio of the repository",
    ["repo_name", "repo_id"],
)

# Volumes
volume_status = Gauge(
    "zerobyte_volume_status",
    "Volume status (1=mounted, 0=unmounted, -1=error)",
    ["volume_name", "volume_id", "volume_type"],
)

# Exporter self-metrics
exporter_scrape_success = Gauge(
    "zerobyte_exporter_scrape_success",
    "Whether the last scrape was successful (1=yes, 0=no)",
)
exporter_scrape_duration = Gauge(
    "zerobyte_exporter_scrape_duration_seconds",
    "Duration of the last scrape in seconds",
)

# ── Helper mappings ─────────────────────────────────────────────────────────────

STATUS_MAP_BACKUP = {
    "success":     1,
    "error":       0,
    "warning":     2,
    "in_progress": 3,
}

STATUS_MAP_REPO = {
    "healthy":   1,
    "error":     0,
    "unknown":   2,
    "doctor":    2,
    "cancelled": 2,
}

STATUS_MAP_VOLUME = {
    "mounted":   1,
    "unmounted": 0,
    "error":    -1,
}


class ZerobyteClient:
    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url.rstrip("/")
        self.username = username
        self.password = password
        self.session  = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def login(self) -> bool:
        """Authenticate and store the session cookie."""
        try:
            resp = self.session.post(
                f"{self.base_url}/api/auth/sign-in/username",
                json={"username": self.username, "password": self.password},
                timeout=10,
            )
            if resp.status_code == 200:
                log.info("Login successful")
                return True
            log.error("Login failed: %s %s", resp.status_code, resp.text[:200])
            return False
        except Exception as e:
            log.error("Login error: %s", e)
            return False

    def get(self, path: str):
        """Perform a GET request; re-authenticate once on 401."""
        url = f"{self.base_url}{path}"
        resp = self.session.get(url, timeout=15)
        if resp.status_code == 401:
            log.warning("Session expired, attempting re-login...")
            if self.login():
                resp = self.session.get(url, timeout=15)
        resp.raise_for_status()
        return resp.json()


# ── Collection functions ────────────────────────────────────────────────────────

def collect_backups(client: ZerobyteClient):
    schedules = client.get("/api/v1/backups")
    for s in schedules:
        labels = [
            s.get("name", ""),
            str(s.get("shortId", "")),
            s.get("volume", {}).get("name", ""),
            s.get("repository", {}).get("name", ""),
        ]
        # Map string status to numeric value
        raw_status = s.get("lastBackupStatus")
        status_val = STATUS_MAP_BACKUP.get(raw_status, -1) if raw_status else -1
        backup_last_status.labels(*labels).set(status_val)

        # Zerobyte returns timestamps in milliseconds
        last_at = s.get("lastBackupAt")
        if last_at:
            backup_last_at.labels(*labels).set(last_at / 1000)

        next_at = s.get("nextBackupAt")
        if next_at:
            backup_next_at.labels(*labels).set(next_at / 1000)

        backup_enabled.labels(*labels).set(1 if s.get("enabled") else 0)


def collect_repositories(client: ZerobyteClient):
    repos = client.get("/api/v1/repositories")
    for r in repos:
        short_id  = r.get("shortId", "")
        repo_name = r.get("name", "")
        repo_type = r.get("type", "")

        status_raw = r.get("status")
        status_val = STATUS_MAP_REPO.get(status_raw, -1) if status_raw else 2
        repo_status.labels(repo_name, short_id, repo_type).set(status_val)

        last_checked = r.get("lastChecked")
        if last_checked:
            repo_last_checked.labels(repo_name, short_id, repo_type).set(last_checked / 1000)

        # Stats endpoint returns cached data — no expensive restic call triggered
        try:
            stats = client.get(f"/api/v1/repositories/{short_id}/stats")
            repo_total_size.labels(repo_name, short_id).set(stats.get("total_size", 0))
            repo_snapshots_count.labels(repo_name, short_id).set(stats.get("snapshots_count", 0))
            repo_compression_ratio.labels(repo_name, short_id).set(stats.get("compression_ratio", 0))
        except Exception as e:
            log.warning("Stats for repository %s unavailable: %s", repo_name, e)


def collect_volumes(client: ZerobyteClient):
    volumes = client.get("/api/v1/volumes")
    for v in volumes:
        status_val = STATUS_MAP_VOLUME.get(v.get("status", ""), -1)
        volume_status.labels(
            v.get("name", ""),
            str(v.get("shortId", "")),
            v.get("type", ""),
        ).set(status_val)


def scrape(client: ZerobyteClient):
    start = time.time()
    try:
        collect_backups(client)
        collect_repositories(client)
        collect_volumes(client)
        exporter_scrape_success.set(1)
        log.info("Scrape successful (%.2fs)", time.time() - start)
    except Exception as e:
        log.error("Scrape failed: %s", e)
        exporter_scrape_success.set(0)
    finally:
        exporter_scrape_duration.set(time.time() - start)


# ── Entry point ─────────────────────────────────────────────────────────────────

def main():
    if not ZEROBYTE_EMAIL or not ZEROBYTE_PASS:
        log.error("ZEROBYTE_EMAIL and ZEROBYTE_PASSWORD must be set!")
        raise SystemExit(1)

    # Optionally unregister default process/platform metrics for a cleaner output:
    # REGISTRY.unregister(PROCESS_COLLECTOR)
    # REGISTRY.unregister(PLATFORM_COLLECTOR)

    client = ZerobyteClient(ZEROBYTE_URL, ZEROBYTE_EMAIL, ZEROBYTE_PASS)

    log.info("Connecting to Zerobyte at %s", ZEROBYTE_URL)
    if not client.login():
        raise SystemExit("Login failed, exporter is shutting down.")

    log.info("Starting HTTP server on port %d", EXPORTER_PORT)
    start_http_server(EXPORTER_PORT)

    while True:
        scrape(client)
        time.sleep(SCRAPE_INTERVAL)


if __name__ == "__main__":
    main()

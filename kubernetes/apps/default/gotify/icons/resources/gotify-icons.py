#!/usr/bin/env python3

import os
import re
import requests

GOTIFY_URL = os.environ["GOTIFY_URL"]
GOTIFY_USER = os.environ["GOTIFY_USERNAME"]
GOTIFY_PASS = os.environ["GOTIFY_PASSWORD"]

CDN_BASE = "https://cdn.jsdelivr.net/gh/homarr-labs/dashboard-icons/png"

ICON_MAPPING = {
    "Change-Detection":  "changedetection",
    "DB-Backup":         "postgresql",
    "Radarr4K":          "radarr-4k",
    "RSS-Forwarder":     "github-light",
    "SonarrKids":        "sonarr",
    "Sonarr4K":          "sonarr-4k",
    "USV":               "apc",
}

SKIP_LIST = [
    "CVE-Report",
]


def get_icon_name(app_name: str) -> str:
    if app_name in ICON_MAPPING:
        return ICON_MAPPING[app_name]
    return re.sub(r"[^a-z0-9]+", "-", app_name.lower()).strip("-")


def app_has_icon(app: dict) -> bool:
    return not app["image"].startswith("static/")


def upload_icon(session: requests.Session, app_id: int, icon_name: str) -> bool:
    url = f"{CDN_BASE}/{icon_name}.png"
    resp = requests.get(url)
    if resp.status_code != 200:
        print(f"  Icon not found: {url}")
        return False

    upload = session.post(
        f"{GOTIFY_URL}/application/{app_id}/image",
        files={"file": (f"{icon_name}.png", resp.content, "image/png")},
    )
    if upload.status_code == 200:
        print(f"  Icon uploaded: {icon_name}.png")
        return True
    else:
        print(f"  Upload failed: {upload.status_code} {upload.text}")
        return False


def main():
    session = requests.Session()
    session.auth = (GOTIFY_USER, GOTIFY_PASS)

    resp = session.get(f"{GOTIFY_URL}/application")
    resp.raise_for_status()
    applications = resp.json()

    print(f"Found {len(applications)} applications")

    for app in applications:
        app_id = app["id"]
        app_name = app["name"]

        print(f"[{app_name}]")

        if app_name in SKIP_LIST:
            print(f"  Skipped (SKIP_LIST)")
            continue

        if app_has_icon(app):
            print(f"  Icon already set, skipping")
            continue

        icon_name = get_icon_name(app_name)
        print(f"  -> {icon_name}")

        upload_icon(session, app_id, icon_name)


if __name__ == "__main__":
    main()

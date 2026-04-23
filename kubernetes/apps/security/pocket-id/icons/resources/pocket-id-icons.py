#!/usr/bin/env python3

import os
import re
import requests

POCKET_ID_URL = os.environ["POCKET_ID_URL"]
POCKET_ID_API_KEY = os.environ["POCKET_ID_API_KEY"]

CDN_BASE = "https://cdn.jsdelivr.net/gh/homarr-labs/dashboard-icons/png"

ICON_MAPPING = {
    "Synapse":        "matrix-synapse-light",
    "OpenPubkey-SSH": "sshwifty",
}

SKIP_LIST = [
    "Toolhive",
]


def get_icon_name(client_name: str) -> str:
    if client_name in ICON_MAPPING:
        return ICON_MAPPING[client_name]
    return re.sub(r"[^a-z0-9]+", "-", client_name.lower()).strip("-")


def client_has_logo(session: requests.Session, client_id: str) -> bool:
    resp = session.get(f"{POCKET_ID_URL}/api/oidc/clients/{client_id}/logo")
    return resp.status_code == 200


def upload_logo(session: requests.Session, client_id: str, icon_name: str) -> bool:
    url = f"{CDN_BASE}/{icon_name}.png"
    resp = requests.get(url)
    if resp.status_code != 200:
        print(f"  Icon not found: {url}")
        return False

    upload = session.post(
        f"{POCKET_ID_URL}/api/oidc/clients/{client_id}/logo",
        files={"file": (f"{icon_name}.png", resp.content, "image/png")},
    )
    if upload.status_code == 204:
        print(f"  Logo uploaded: {icon_name}.png")
        return True
    else:
        print(f"  Upload failed: {upload.status_code} {upload.text}")
        return False


def get_all_clients(session: requests.Session) -> list:
    clients = []
    page = 1
    while True:
        resp = session.get(
            f"{POCKET_ID_URL}/api/oidc/clients",
            params={"page": page},
        )
        resp.raise_for_status()
        data = resp.json()
        clients.extend(data["data"])
        if page >= data["pagination"]["totalPages"]:
            break
        page += 1
    return clients


def main():
    session = requests.Session()
    session.headers["X-API-Key"] = POCKET_ID_API_KEY

    clients = get_all_clients(session)

    print(f"Found {len(clients)} clients")

    for client in clients:
        client_id = client["id"]
        client_name = client["name"]

        print(f"[{client_name}]")

        if client_name in SKIP_LIST:
            print(f"  Skipped (SKIP_LIST)")
            continue

        if client_has_logo(session, client_id):
            print(f"  Logo already set, skipping")
            continue

        icon_name = get_icon_name(client_name)
        print(f"  -> {icon_name}")

        upload_logo(session, client_id, icon_name)


if __name__ == "__main__":
    main()

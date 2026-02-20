#!/usr/bin/env python3

import os
import json
import logging
import argparse
from datetime import date, timedelta

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# ─── Konfiguration ────────────────────────────────────────────────────────────

CONFIG = {
    "calendar_id":       os.getenv("CALENDAR_ID", "primary"),
    "exclude_label":     os.getenv("EXCLUDE_LABEL", "no-birthday"),
    "google_token_json": os.getenv("GOOGLE_TOKEN_JSON"),
}

SCOPES = [
    "https://www.googleapis.com/auth/contacts.readonly",
    "https://www.googleapis.com/auth/calendar.events",
]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)

CURRENT_YEAR = date.today().year


# ─── Hilfsfunktion ────────────────────────────────────────────────────────────

def build_key(name: str, day: int, month: int, birth_year: int | None) -> str:
    """Eindeutiger Key für den Diff-Abgleich."""
    if birth_year:
        return f"{name}_{day:02d}.{month:02d}.{birth_year}_{CURRENT_YEAR}"
    else:
        return f"{name}_{day:02d}.{month:02d}_{CURRENT_YEAR}"


# ─── Google Auth ──────────────────────────────────────────────────────────────

def get_credentials() -> Credentials:
    token_json = CONFIG["google_token_json"]
    if not token_json:
        raise RuntimeError("GOOGLE_TOKEN_JSON ist nicht gesetzt!")

    creds = Credentials.from_authorized_user_info(json.loads(token_json), SCOPES)

    if not creds.valid:
        if creds.expired and creds.refresh_token:
            log.info("Token wird erneuert...")
            creds.refresh(Request())
        else:
            raise RuntimeError(
                "Token ist ungültig. Bitte lokal neu authentifizieren "
                "und GOOGLE_TOKEN_JSON in 1Password aktualisieren."
            )

    return creds


# ─── Google Contacts ──────────────────────────────────────────────────────────

def get_excluded_contact_ids(people_service) -> set:
    exclude_label = CONFIG["exclude_label"].lower()
    excluded_ids = set()

    try:
        groups = people_service.contactGroups().list().execute().get("contactGroups", [])
        target_group = next(
            (g for g in groups if g.get("name", "").lower() == exclude_label),
            None
        )

        if not target_group:
            log.info(f"Label '{CONFIG['exclude_label']}' nicht gefunden – kein Kontakt wird ausgeschlossen.")
            return excluded_ids

        log.info(f"Label '{target_group['name']}' gefunden ({target_group['resourceName']})")

        group_detail = people_service.contactGroups().get(
            resourceName=target_group["resourceName"],
            maxMembers=1000,
        ).execute()

        excluded_ids = set(group_detail.get("memberResourceNames", []))
        log.info(f"{len(excluded_ids)} Kontakte werden ausgeschlossen.")

    except HttpError as e:
        log.warning(f"Fehler beim Laden der Labels: {e}")

    return excluded_ids


def get_birthdays(people_service, excluded_ids: set) -> dict[str, dict]:
    """Gibt ein Dict zurück: { event_key → birthday_dict }"""
    birthdays = {}
    page_token = None

    while True:
        kwargs = {
            "resourceName": "people/me",
            "pageSize": 1000,
            "personFields": "names,birthdays",
        }
        if page_token:
            kwargs["pageToken"] = page_token

        result = people_service.people().connections().list(**kwargs).execute()

        for person in result.get("connections", []):
            if person.get("resourceName", "") in excluded_ids:
                continue

            names = person.get("names", [])
            if not names:
                continue

            display_name = names[0].get("displayName", "").strip()
            if not display_name:
                continue

            for bday in person.get("birthdays", []):
                bday_date = bday.get("date", {})
                month = bday_date.get("month")
                day = bday_date.get("day")
                birth_year = bday_date.get("year")  # kann None sein

                if month and day:
                    age = CURRENT_YEAR - birth_year if birth_year else None
                    key = build_key(display_name, day, month, birth_year)
                    birthdays[key] = {
                        "name": display_name,
                        "month": month,
                        "day": day,
                        "birth_year": birth_year,
                        "age": age,
                        "key": key,
                    }

        page_token = result.get("nextPageToken")
        if not page_token:
            break

    log.info(f"{len(birthdays)} Geburtstage aus Google Contacts geladen.")
    return birthdays


# ─── Google Calendar ──────────────────────────────────────────────────────────

def get_existing_birthday_events(calendar_service) -> dict[str, str]:
    """Gibt ein Dict zurück: { event_key → event_id }"""
    existing = {}
    page_token = None

    while True:
        kwargs = {
            "calendarId": CONFIG["calendar_id"],
            "privateExtendedProperty": "source=birthday-sync",
            "maxResults": 2500,
            "singleEvents": False,
        }
        if page_token:
            kwargs["pageToken"] = page_token

        try:
            result = calendar_service.events().list(**kwargs).execute()
        except HttpError as e:
            log.warning(f"Fehler beim Laden bestehender Events: {e}")
            break

        for event in result.get("items", []):
            props = event.get("extendedProperties", {}).get("private", {})
            event_key = props.get("event_key")
            if event_key:
                existing[event_key] = event["id"]

        page_token = result.get("nextPageToken")
        if not page_token:
            break

    log.info(f"{len(existing)} bestehende Geburtstags-Events im Kalender.")
    return existing


def delete_event(calendar_service, event_id: str, key: str, dry_run: bool) -> bool:
    if dry_run:
        log.info(f"[DRY-RUN] Würde löschen: {key}")
        return True
    try:
        calendar_service.events().delete(
            calendarId=CONFIG["calendar_id"],
            eventId=event_id,
        ).execute()
        log.info(f"🗑 Gelöscht: {key}")
        return True
    except HttpError as e:
        log.error(f"Fehler beim Löschen von {key}: {e}")
        return False


def create_event(calendar_service, birthday: dict, dry_run: bool) -> bool:
    name = birthday["name"]
    month = birthday["month"]
    day = birthday["day"]
    age = birthday.get("age")
    birth_year = birthday.get("birth_year")

    try:
        event_date = date(CURRENT_YEAR, month, day)
    except ValueError:
        event_date = date(CURRENT_YEAR, month, 28)
        log.warning(f"{name}: 29. Feb → 28. Feb angepasst")

    date_str = event_date.strftime("%Y-%m-%d")
    next_day_str = (event_date + timedelta(days=1)).strftime("%Y-%m-%d")

    summary = f"🎂 {name} ({age})" if age is not None else f"🎂 {name}"
    description = f"Geburtstag von {name}" + (f"\nGeboren: {birth_year}" if birth_year else "")

    event_body = {
        "summary": summary,
        "description": description,
        "start": {"date": date_str},
        "end": {"date": next_day_str},
        "reminders": {"useDefault": True},
        "transparency": "transparent",
        "extendedProperties": {
            "private": {
                "source": "birthday-sync",
                "contact_name": name,
                "event_key": birthday["key"],
            }
        },
    }

    if dry_run:
        log.info(f"[DRY-RUN] Würde erstellen: {summary} ({day:02d}.{month:02d}.)")
        return True

    try:
        calendar_service.events().insert(
            calendarId=CONFIG["calendar_id"],
            body=event_body,
        ).execute()
        log.info(f"✓ Erstellt: {summary} ({day:02d}.{month:02d}.)")
        return True
    except HttpError as e:
        log.error(f"✗ Fehler bei {name}: {e}")
        return False


# ─── Hauptprogramm ────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Google Contacts → Google Calendar Birthday Sync")
    parser.add_argument("--dry-run", action="store_true",
                        help="Nichts schreiben oder löschen, nur anzeigen was passieren würde")
    parser.add_argument("--list-contacts", action="store_true",
                        help="Alle Kontakte mit Geburtstag auflisten und beenden")
    args = parser.parse_args()

    log.info("=== Birthday Sync gestartet ===")
    if args.dry_run:
        log.info("DRY-RUN Modus – keine Änderungen werden vorgenommen")

    creds = get_credentials()
    people_service = build("people", "v1", credentials=creds)
    calendar_service = build("calendar", "v3", credentials=creds)

    excluded_ids = get_excluded_contact_ids(people_service)
    contacts_birthdays = get_birthdays(people_service, excluded_ids)

    if args.list_contacts:
        print("\n📋 Kontakte mit Geburtstag:")
        for b in sorted(contacts_birthdays.values(), key=lambda x: (x["month"], x["day"])):
            age_str = f" → wird {b['age']}" if b.get("age") else ""
            print(f"  {b['day']:02d}.{b['month']:02d}  {b['name']}{age_str}")
        return

    calendar_events = get_existing_birthday_events(calendar_service)

    contacts_keys = set(contacts_birthdays.keys())
    calendar_keys = set(calendar_events.keys())

    to_create = contacts_keys - calendar_keys
    to_delete = calendar_keys - contacts_keys
    unchanged = contacts_keys & calendar_keys

    log.info(f"Diff: {len(to_create)} neu, {len(to_delete)} zu löschen, {len(unchanged)} unverändert")

    deleted = sum(
        delete_event(calendar_service, calendar_events[key], key, args.dry_run)
        for key in to_delete
    )

    created = sum(
        create_event(calendar_service, contacts_birthdays[key], args.dry_run)
        for key in to_create
    )

    log.info(f"=== Fertig: {created} erstellt, {deleted} gelöscht, {len(unchanged)} unverändert ===")


if __name__ == "__main__":
    main()
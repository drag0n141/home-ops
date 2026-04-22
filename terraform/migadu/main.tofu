terraform {
  required_providers {
    migadu = {
      source  = "metio/migadu"
      version = "2026.3.5"
    }
  }
}

variable "domain" {
  type = string
}

variable "app" {
  type = string
}

variable "name" {
  type = string
}

variable "destination_local_part" {
  type = string
}

resource "migadu_identity" "identity" {
  domain_name  = var.domain
  local_part   = var.destination_local_part
  identity     = var.app
  name         = var.name
  password_use = "none"
  may_send     = true
}

resource "migadu_alias" "alias" {
  domain_name  = var.domain
  local_part   = var.app
  destinations = ["${var.destination_local_part}@${var.domain}"]
}

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

resource "random_password" "password" {
  length = 64
}

resource "migadu_mailbox" "mailbox" {
  name        = var.name
  domain_name = var.domain
  local_part  = var.app
  password    = random_password.password.result
  may_send    = true
}

output "password" {
  sensitive = true
  value = random_password.password.result
}

output "host" {
  value = "smtp.migadu.com"
}
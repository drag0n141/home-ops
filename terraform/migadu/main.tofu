terraform {
  required_providers {
    migadu = {
      source  = "metio/migadu"
      version = "2026.3.5"
    }
    onepassword = {
      source  = "1Password/onepassword"
      version = "2.2.1"
    }
  }
}

provider "onepassword" {
  url   = var.OP_CONNECT_HOST
  token = var.OP_CONNECT_TOKEN
}

data "onepassword_vault" "kubernetes" {
  name = "Kubernetes"
}

module "onepassword_migadu" {
  source = "github.com/joryirving/terraform-1password-item"
  vault  = data.onepassword_vault.kubernetes.name
  item   = "migadu"
  providers = {
    onepassword = onepassword
  }
}

provider "migadu" {
  username = module.onepassword_migadu.fields["MIGADU_USERNAME"]
  token    = module.onepassword_migadu.fields["MIGADU_TOKEN"]
}

locals {
  identities = [
    { app = "authentik",       name = "Authentik" },
    { app = "bitwarden",       name = "Bitwarden" },
    { app = "books",           name = "Books" },
    { app = "cve-report",      name = "CVE-Report" },
    { app = "epicgames",       name = "EpicGames" },
    { app = "ferdium",         name = "Ferdium" },
    { app = "git",             name = "Git" },
    { app = "immich",          name = "Immich" },
    { app = "kitchenowl",      name = "Kitchenowl" },
    { app = "matrix",          name = "Matrix" },
    { app = "nas01",           name = "NAS01" },
    { app = "netbox",          name = "Netbox" },
    { app = "nextcloud",       name = "Nextcloud" },
    { app = "outline",         name = "Outline" },
    { app = "pocket-id",       name = "Pocket-ID" },
    { app = "rss",             name = "RSS" },
    { app = "tautulli",        name = "Tautulli" },
    { app = "unifi",           name = "Unifi" },
    { app = "wallos",          name = "Wallos" },
    { app = "wiki",            name = "Wiki" },
    { app = "wireguard",       name = "Wireguard Portal" },
  ]
}
module "identities" {
  for_each               = { for i in local.identities : i.app => i }
  source                 = "./modules/migadu"
  app                    = each.value.app
  name                   = each.value.name
  domain                 = var.domain
  destination_local_part = var.destination_local_part
}

terraform {
  required_providers {
    onepassword = {
      source  = "1Password/onepassword"
      version = "3.3.1"
    }

    gotify = {
      source  = "LukasKnuth/gotify"
      version = "0.3.0"
    }
  }
}

provider "onepassword" {
  connect_url   = var.OP_CONNECT_HOST
  connect_token = var.OP_CONNECT_TOKEN
}

data "onepassword_vault" "kubernetes" {
  name = "Kubernetes"
}

module "onepassword_gotify" {
  source = "github.com/joryirving/terraform-1password-item"
  vault  = data.onepassword_vault.kubernetes.name
  item   = "gotify"

  providers = {
    onepassword = onepassword
  }
}

provider "gotify" {
  endpoint = "http://gotify.default.svc.cluster.local"
  username = module.onepassword_gotify.fields["GOTIFY_DEFAULTUSER_NAME"]
  password = module.onepassword_gotify.fields["GOTIFY_DEFAULTUSER_PASS"]
}

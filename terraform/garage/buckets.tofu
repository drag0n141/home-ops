locals {
  buckets = [
    "cnpg",
    "k8s",
    "lisa",
    "mariadb",
    "opnsense",
    "sven",
  ]
}

resource "garage_key" "admin_key" {
  name = "admin-user"
}

module "buckets" {
  for_each    = toset(local.buckets)
  source      = "./modules/garage"
  bucket_name = each.key
  admin_user  = garage_key.admin_key.id

  providers = {
    garage = garage
  }
}

import {
  to = module.buckets["cnpg"].garage_bucket.bucket
  id = "36d843a4e273a349"
}

import {
  to = module.buckets["k8s"].garage_bucket.bucket
  id = "39c8777ddb6e371b"
}

import {
  to = module.buckets["lisa"].garage_bucket.bucket
  id = "81e8f324cfd2fcc1"
}

import {
  to = module.buckets["mariadb"].garage_bucket.bucket
  id = "0b86c4124be46d0b"
}

import {
  to = module.buckets["opnsense"].garage_bucket.bucket
  id = "9ce43ca653b80644"
}

import {
  to = module.buckets["sven"].garage_bucket.bucket
  id = "73fc0908ce9f4fe7"
}

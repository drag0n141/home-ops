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
  id = "36d843a4e273a3492842f1c6ae66e99f2ad5f9dae6da4775b0c7ee795685594c"
}

import {
  to = module.buckets["k8s"].garage_bucket.bucket
  id = "39c8777ddb6e371b5bad1b94d482e80b5296ed039eb9f2d9343197ffd1bbd73f"
}

import {
  to = module.buckets["lisa"].garage_bucket.bucket
  id = "81e8f324cfd2fcc19f2c7b7c2b89d9eb575d657e34c5e9d1fcd91a255fdaa278"
}

import {
  to = module.buckets["mariadb"].garage_bucket.bucket
  id = "0b86c4124be46d0b499bfa7b346d33616cc16f37f19aa0ba9a477e41a0710d94"
}

import {
  to = module.buckets["opnsense"].garage_bucket.bucket
  id = "9ce43ca653b80644b412156c2dc14ee0386e179abcd05b516cff6882d2bf483a"
}

import {
  to = module.buckets["sven"].garage_bucket.bucket
  id = "73fc0908ce9f4fe75013d327b346c169331ad62971ef29510f164a0ad4e34482"
}

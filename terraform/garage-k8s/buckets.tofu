locals {
  buckets = [
    "forgejo",
    "netbox",
    "outline",
    "zipline",
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
  to = module.buckets["netbox"].garage_bucket.bucket
  id = "0a8503082f1e6fa6d2b1ee9d5d30bd92d2f0a986aa357b71df628602bb90b875"
}

import {
  to = module.buckets["outline"].garage_bucket.bucket
  id = "aaf04c3c8a1b4a0a132cebd9835decf0555fd6f050750aa85325214eba0e81e4"
}

import {
  to = module.buckets["zipline"].garage_bucket.bucket
  id = "03c7e4aa2a8cae4c5d3b267ca1606bbbe931ed07a426af4acae4bc0cd61df0ab"
}

import {
  to = module.buckets["forgejo"].garage_bucket.bucket
  id = "0a9d82bcbd60225c786fb660db9eab6e8b3200c7c9fdaccdc79cac0030aab4b6"
}

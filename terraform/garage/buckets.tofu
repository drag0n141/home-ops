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

# Admin key for managing garage buckets
resource "garage_key" "admin_key" {
  name = "admin-user"
}

# Create buckets dynamically using the garage module
module "buckets" {
  for_each    = toset(local.buckets)
  source      = "./modules/garage"
  bucket_name = each.key
  admin_user  = garage_key.admin_key.id

  providers = {
    garage = garage
  }
}

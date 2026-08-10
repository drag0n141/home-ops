variable "OP_CONNECT_HOST" {
  type = string
}

variable "OP_CONNECT_TOKEN" {
  type      = string
  sensitive = true
  default   = null
}

variable "app_token_overrides" {
  description = "One-time manual overrides for app tokens recovered outside of Terraform (e.g. re-copied from the 1Password item after they were regenerated in the Gotify web UI), keyed by application name. Only needed to seed terraform_data.app_token_cache once after a token was lost to the Gotify 3.0 GET regression. Safe to leave populated afterwards - ignore_changes on the cache means it's only read on the apply where the cache doesn't have a value yet."
  type        = map(string)
  default     = {}
}

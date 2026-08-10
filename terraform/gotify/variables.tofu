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

variable "cache_generation" {
  description = "Bump this (any new distinct string) to force terraform_data.app_token_cache to be destroyed and recreated instead of updated in place. Needed because ignore_changes on the cache's `input` blocks normal updates - including a legitimate app_token_overrides seed - once the cache already holds a (possibly empty) value. A replace re-evaluates `input` fresh, since it's a brand new resource instance. Do not bump this casually: whatever app_token_overrides (or the live Gotify token, which is empty post-3.0) resolves to at the moment of the bump becomes the new permanently-cached value."
  type        = string
  default     = "1"
}

variable "OP_CONNECT_HOST" {
  type = string
}

variable "OP_CONNECT_TOKEN" {
  type      = string
  sensitive = true
}

variable "domain" {
  type = string
}

variable "destination_local_part" {
  type = string
}

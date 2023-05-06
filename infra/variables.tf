variable "PROJECT_ID" {
  type        = string
  description = "This is an example input variable using env variables."
}

variable "region" {
  default = "us-central1"
}

variable "zone" {
  default = "us-central1-c"
}
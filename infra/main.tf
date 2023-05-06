terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
}

//Main GCP Diagonstics
provider "google" {
  project = var.PROJECT_ID
  region  = var.region
  zone    = var.zone
}

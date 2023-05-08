terraform {
  cloud {
    organization = "jamesn9"

    workspaces {
      name = "gcp-infra"
    }
  }
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
}

provider "google" {
  project = var.PROJECT_ID
  region  = var.region
  zone    = var.zone
}

data "google_project" "project" {
}


module "lending_originations" {
  source = "./lending_originations"
}

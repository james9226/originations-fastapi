# Originations FastAPI Demo Project

![CI](https://github.com/james9226/originations-fastapi/actions/workflows/ci.yaml/badge.svg
) ![CD](https://github.com/james9226/originations-fastapi/actions/workflows/cd.yaml/badge.svg
)

This is a FastAPI project, containerized with docker and hosted on GCP cloud run.

It uses GitHub actions for a simple CI/CD flow and google secrets manager for secrets management.
Environment variables are stored in the CD script, injected into the container at deploy time with the cloud run deploy command and are managed at runtime with the Pydantic Settings class.

## Project Structure

    .
    ├── pyproject.toml             # App Dependancies
    ├── /tests                     # Test files (alternatively `spec` or `tests`)
    │
    ├── /originations              # Infrastructure (Terraform) configuration
    │   ├── main.py                # FastAPI application entrypoint
    │   ├── /config                # Environment and configuration used throughout the app
    │   ├── /domain                # Domain functions used to decision an application
    │   ├── /enums                 # Common enums used through the app
    │   ├── /middleware            # Logging and context middleware for the app
    │   ├── /models                # Pydantic Data models used throughout the app
    │   └── /services              # External (sometimes mocked) services that the app interacts with
    │
    ├── /infra                     # Infrastructure (Terraform) configuration
    │   ├── /functions             # Helper functions used in terraform pipelie
    │   ├── /lending_originations  # Configuration for lending_originations dataset tables + pipelines
    │   └── unit                   # Unit tests
    │
    └── /docs                      # Documentation for the project


## Infrastructure

![Infra Diagram](https://github.com/james9226/originations-fastapi/blob/main/docs/Infrastructure.drawio.png?raw=true)

The Infrastructure used is as follows:

- Cloud Run hosts a Dockerized Python FastAPI application, which is a monolithic application serving all requests. 
- Cloud Firestore is used as a production DB
- Pub/Sub is used to stream reporting events to BigQuery in realtime
- Terraform is used to configure both Pub/Sub and the resultant BigQuery tables 
- GitHub actions automates the CI suite:
  - PyTest
  - MyPy
  - Snyk Vulnerability Scanning
  - Terraform Validation / Planning
- GitHub actions also automates the CD suite:
  - Docker Build -> Cloud Registry -> Deploy pipeline for the main app
  - Terraform 
- Google Secrets Manager for sensitive credentials
- Cloud IAM for access management

## Run Locally

You should have poetry and python already installed on your machine!

Run `poetry env use 3.10` to create the virtual environment

Run `poetry install --with dev` to install the project's dependancies, including dev dependancies

Run `gcloud auth application-default login` to authenticate with google cloud

Run `poetry run uvicorn originations.main:app --reload` to run the API locally in development mode (not dockerised)

## Project Configuration

### Secrets

- Google Secrets Manager for the following secrets:
  - originations-api-key (basic auth password for the API)
  - firebase_private_key
- GitHub Actions Secrets containing:
  - GitHub Service Account Key
  - Synk Token

### IAM Configuration

- Google Compute Service Account needs to be granted READ permissions on Secrets Manager
- Service Account create for GitHub needs the following permissions:
  - Cloud Run Developer
  - Artifact Registry Add/Push
  - It also needs to be registered as a permitted user of the service account for cloud run!
  
## TODO

- Migrate production from Cloud Firestore to Cloud SQL (or other SQL DB)
- Fully configure production DB, IAM, Secrets and Cloud Run in Terraform
- Enable CodeQL for ongoing vulenerability scanning of main branch
- Finish the main application!!
- Build a frontend!

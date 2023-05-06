# Originations FastAPI Demo Project

![CI](https://github.com/james9226/originations-fastapi/actions/workflows/ci.yaml/badge.svg
) ![CD](https://github.com/james9226/originations-fastapi/actions/workflows/cd.yaml/badge.svg
)

This is a FastAPI project, containerized with docker and hosted on GCP cloud run.

It uses GitHub actions for a simple CI/CD flow and google secrets manager for secrets management.
Environment variables are stored in the CD script, injected into the container at deploy time with the cloud run deploy command and are managed at runtime with the Pydantic Settings class.

## Run Locally

You should have poetry and python already installed on your machine!

Run `poetry env use 3.9` to create the virtual environment

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

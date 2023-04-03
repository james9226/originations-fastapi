# Originations FastAPI Demo Project

![CI](https://github.com/james9226/originations-fastapi/actions/workflows/ci.yaml/badge.svg
) ![CD](https://github.com/james9226/originations-fastapi/actions/workflows/cd.yaml/badge.svg
)


This is a FastAPI project, containerized with docker and hosted on GCP cloud run

It uses GitHub actions for a simple CI/CD flow, and uses google secrets manager. 

## Project Configuration

### Secrets

- Google Secrets Manager for the following secrets:
  - originations-api-key (basic auth password for the API)
  - firebase_private_key_id
  - firebase_private_key
  - firebase_client_email
- GitHub Actions Secrets containing:
  - GitHub Service Account Key 
  - Synk Token

### IAM Configuration

- Google Compute Service Account needs to be granted READ permissions on Secrets Manager
- Service Account create for GitHub needs the following permissions:
  - Cloud Run Developer
  - Artifact Registry Add/Push 
  - It also needs to be registered as a permitted user of the service account for cloud run! 

# Originations FastAPI Demo Project

![CI](https://github.com/james9226/originations-fastapi/actions/workflows/ci.yaml/badge.svg
) ![CD](https://github.com/james9226/originations-fastapi/actions/workflows/cd.yaml/badge.svg
)

This is a FastAPI project, containerized with docker and hosted on GCP cloud run.

It uses GitHub actions for a simple CI/CD flow and google secrets manager for secrets management.
Environment variables are stored in the CD script, injected into the container at deploy time with the cloud run deploy command and are managed at runtime with the Pydantic Settings class.

- [Originations FastAPI Demo Project](#originations-fastapi-demo-project)
  - [Project Structure](#project-structure)
  - [Endpoints](#endpoints)
  - [Application Architecture](#application-architecture)
    - [Usage of Async](#usage-of-async)
    - [Triggers State Store](#triggers-state-store)
    - [Bureau Service](#bureau-service)
  - [Infrastructure](#infrastructure)
  - [Run Locally](#run-locally)
  - [Project Configuration](#project-configuration)
    - [Secrets](#secrets)
    - [IAM Configuration](#iam-configuration)
  - [TODO](#todo)

## Project Structure

    .
    ├── pyproject.toml             # App Dependancies
    ├── /tests                     # Test files (alternatively `spec` or `tests`)
    ├── /.github/workflows         # CI/CD pipeline configuration
    │
    ├── /originations              # The Originations App!
    │   ├── main.py                # FastAPI application entrypoint
    │   ├── /config                # Environment and configuration used throughout the app
    │   ├── /domain                # Domain functions used to decision an application
    │   ├── /enums                 # Common enums used through the app
    │   ├── /middleware            # Logging and context middleware for the app
    │   ├── /models                # Pydantic Data models used throughout the app
    │   └── /services              # External (sometimes mocked) services that the app interacts with
    │
    ├── /infra                     # Infrastructure (Terraform) configuration
    │   ├── .                      # Primary terraform configuration
    │   ├── /functions             # Helper functions used in terraform pipelie
    │   └── /lending_originations  # Configuration for lending_originations dataset tables + pipelines
    │
    └── /docs                      # Documentation for the project

## Endpoints

- /docs/ - Swagger documentation
- /v1/application/ - Application (Quotation) Endpoint (under construction)
- /v1/submission/ - Submission (Hard Search) Endpoint (tbd)

## Application Architecture

![Application Diagram](https://github.com/james9226/originations-fastapi/blob/main/docs/quotation.drawio.png?raw=true)

### Usage of Async 

We use simulatenous async writes where possible, e.g. in the prevetting stage we:
- Log applicant PII to production DB
- Log the application request to pub/sub
- Run prevetting policy
Asnchronously at the same time!

This allows the API to be very fast (700ms response for someone declined at prevetting, 1.2-2.2 seconds for a quotation)

### Triggers State Store

While we publish the results of all our policy rules to pub/sub for ingestion to BigQuery, we also maintain one document per applicant hash (a unique ID for each combination of PII) that contains a map of all policy rules the applicant has ever triggered and when the rule was most recently triggered. This minimizes the amount of data we need to write to a DB (slower than publishing to a topic) and enables very efficient DB reads, as there is only one document that ever needs to be grabbed, which can be fetched by its exact document ID (the hash) and which contains the relevant data for deciding whether to decline the application due to recent declines. This minimizes the need to pull fresh files if they were recently declined, saving bureau costs.

### Bureau Service

We also cache credit files and use the bureau service to handle this. It will first check the DB for the credit file (again according to the exact document reference) and, iff it does not find one, it will then fetch a new file from a (mocked) bureau endpoint and write it to the DB for future usage.

TODO: Refactor this implementation

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
- Fix MyPy so the project is fully type-safe (currently disabled)

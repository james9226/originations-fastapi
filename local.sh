#!/bin/sh

gcloud auth application-default login 

poetry run uvicorn originations.main:app --reload
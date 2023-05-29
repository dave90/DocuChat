# Text To Vector Service

This micro service store a large text to the DB Vector that will
be used during the query answer phase.

# Dependencies
This service depends on *DB vector* service.

Please install the python dependencies from *requirements.txt*

# Docker

## Build

- local: docker build -t text-to-vec .
- azure: 
  - AZURE_REPO=\<Your azure docker repo name\>
  - az acr build -r $AZURE_REPO -t text-to-vec .

# Environment variables
- DBVECTOR_SERVICE_NAME: Name or IP of the DbVector service
- DBVECTOR_SERVICE_PORT: Open port of the DbVector service


# To run locally

uvicorn main:app --reload --port 8000

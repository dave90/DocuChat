# To run
uvicorn main:app --reload --port 8000

# Docker

## Build

- local: docker build -t text-to-vec .
- azure: az acr build -r \<azure docker repo name\> -t text-to-vec .

## Run

- docker run -p 8000:8000 text-to-vec 

# Create requirements
pip freeze > requirements.txt

# Environment variables
- DBVECTOR_SERVICE_NAME: name of the DbVector service
- DBVECTOR_SERVICE_PORT: Open port of the DbVector service
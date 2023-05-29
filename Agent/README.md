# Agent Service

This micro service manage the query answering with the documents agent.

# Dependencies
This service depends on *DB vector* service.

Please install the python dependencies from *requirements.txt*

# Docker

## Build

- local: docker build -t agent .
- azure: 
  - AZURE_REPO=\<Your azure docker repo name\>
  - az acr build -r $AZURE_REPO -t agent .


# Environment variables:
- OPENAI_API_KEY: OpenAI API key
- DBVECTOR_SERVICE_NAME: Name or IP of the DbVector service
- DBVECTOR_SERVICE_PORT: Open port of the DbVector service


# To run locally:
uvicorn main:app --reload --port 8002


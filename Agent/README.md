# To run:
uvicorn main:app --reload --port 8002


# Docker

## Build

- local: docker build -t agent .
- azure: az acr build -r \<azure docker repo name\> -t agent .

## Run

- docker run -p 8002:8002 agent
- 
# Create requirements:
pip freeze > requirements.txt

# Environment variables:
- OPENAI_API_KEY: OpenAI API key
- DBVECTOR_SERVICE_NAME: name of the DbVector service
- DBVECTOR_SERVICE_PORT: Open port of the DbVector service

# To run:
uvicorn main:app --reload --port 8001


# Docker

## Build

- local: docker build -t db-vec .
- azure: az acr build -r \<azure docker repo name\> -t db-vec .

## Run

- docker run -p 8001:8001 db-vec

# Create requirements:
pip freeze > requirements.txt

# Environment variables:
- OPENAI_API_KEY: OpenAI API key

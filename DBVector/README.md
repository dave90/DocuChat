# DB Vector Service

This micro service manage the connection (get and store) with the DB Vector.

# Dependencies

Please install the python dependencies from *requirements.txt*

# Docker

## Build

- local: docker build -t db-vec .
- azure: 
  - AZURE_REPO=\<Your azure docker repo name\>
  - az acr build -r $AZURE_REPO -t db-vec .

# Environment variables:
- OPENAI_API_KEY: OpenAI API key
- REDIS_HOST: Redis hsotname
- REDIS_PORT: Redis port

# Run

## Run redis service locally:

- docker run -d --name redis-stack-server -p 6379:6379 redis/redis-stack-server:latest

Get IP of redis docker service:
- docker inspect redis-stack-server | grep IPAddress

## To run locally:

uvicorn main:app --reload --port 8001


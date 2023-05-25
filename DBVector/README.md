# To run:
uvicorn main:app --reload --port 8001


# Docker

## Build

- local: docker build -t db-vec .
- azure: az acr build -r \<azure docker repo name\> -t db-vec .

## Run
- REDIS_HOST=<redis host>
- REDIS_PORT=<redis port>
- OPENAI_API_KEY=<OPEN AI TOKEN>
- docker run -p 8001:8001  -e REDIS_HOST=$REDIS_HOST -e REDIS_PORT=$REDIS_PORT -e OPENAI_API_KEY=$OPENAI_API_KEY db-vec

Run redis service:

- docker run -d --name redis-stack-server -p 6379:6379 redis/redis-stack-server:latest


# Create requirements:
pip freeze > requirements.txt

# Environment variables:
- OPENAI_API_KEY: OpenAI API key
- REDIS_HOST: Redis hsotname
- REDIS_PORT: Redis port

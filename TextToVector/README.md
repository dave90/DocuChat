# To run:
uvicorn main:app --reload --port 8000

# Create requirements:
conda list -e > requirements.txt

# Environment variables:
- DBVECTOR_SERVICE_NAME: name of the DbVector service
- DBVECTOR_SERVICE_PORT: Open port of the DbVector service
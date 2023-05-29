#!/bin/bash
# Service must be deployed in: http://<domain>/text-to-vec:8000
# If you want to change port or service name update the --port and --root-path options

uvicorn main:app --host 0.0.0.0 --port 8000 --root-path /text-to-vec

#!/usr/bin/env bash
set -e
docker build -t admin-only-forum .
docker rm -f admin-only-forum >/dev/null 2>&1 || true
docker run --name admin-only-forum --env-file .env -p 5000:5000 admin-only-forum

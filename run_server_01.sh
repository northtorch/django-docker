#!/usr/bin/ bash
SECRET_KEY=`python get_random_secret_key.py`
docker run --rm -p 8000:8000 -e SECRET_KEY=$SECRET_KEY --name dd-server-01 dd/server:latest
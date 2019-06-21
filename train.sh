#!/usr/bin/env bash

# If the rasa/rasa image version is updated also update the version in the Dockerfile-rasa file!
docker run \
  -v $(pwd):/app/project \
  -v $(pwd)/models:/app/models \
  rasa/rasa:1.0.1-spacy-en \
  train \
    --domain project/config/domain.yml \
    --data project/data \
    --config project/config/config.yml \
    --out models \
    --augmentation 50
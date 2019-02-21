#! /bin/bash -x
set -ex

IMAGE_NAME="habra_proxy"

docker build -t "$IMAGE_NAME" .
docker run -i "$IMAGE_NAME" mypy app tests
docker run -i "$IMAGE_NAME" pytest --isort --flake8

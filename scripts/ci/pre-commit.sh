#! /bin/sh

poetry install --no-dev --no-interaction --no-ansi

pre-commit run -a

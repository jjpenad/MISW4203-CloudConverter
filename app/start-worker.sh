#!/bin/bash

set -o errexit
set -o nounset

celery -A run worker --loglevel INFO
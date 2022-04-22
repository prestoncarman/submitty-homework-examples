#!/bin/bash

# Runs all formatting programs on repo
black .
isort .
codespell -f -w .
flake8 .

# Clean up
find . -name ".pytest_cache" -type d -exec /bin/rm -rf {} +
find . -name "__pycache__" -type d -exec /bin/rm -rf {} +

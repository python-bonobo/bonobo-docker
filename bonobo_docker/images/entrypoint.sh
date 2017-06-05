#!/bin/bash

# Install vendors.
for vendor in `find src -maxdepth 2 -name setup.py | xargs -n1 dirname 2>/dev/null`; do
    echo "Installing $vendor ..."
    pip install -e $vendor
done

# Delegate to user command.
exec "$@"

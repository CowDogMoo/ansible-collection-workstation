#!/bin/bash
set -ex

if [ -z "$1" ]; then
    echo "No username provided"
    exit 1
fi

export ASDF_PATH="/home/$1/.asdf"
export PATH="$ASDF_PATH/bin:$ASDF_PATH/shims:$PATH"

# Check if ASDF_PATH is correctly set
if [[ ! -d "$ASDF_PATH" ]]; then
    echo "ASDF_PATH '$ASDF_PATH' does not exist"
    exit 1
fi

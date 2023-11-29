#!/bin/bash
set -e

export ASDF_PATH="/home/$1/.asdf"
export PATH="$ASDF_PATH/bin:$ASDF_PATH/shims:$PATH"
. "$ASDF_PATH/asdf.sh"
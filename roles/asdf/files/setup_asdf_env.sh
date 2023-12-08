#!/bin/bash
echo "Running setup_asdf_env.sh with user home path: $1"

if [ -z "$1" ]; then
	echo "No user home path provided" >&2
	exit 1
fi

export ASDF_PATH="$1/.asdf"
export PATH="$ASDF_PATH/bin:$ASDF_PATH/shims:$PATH"

echo "Set ASDF_PATH to: $ASDF_PATH"

if [[ ! -d "$ASDF_PATH" ]]; then
	echo "ASDF_PATH '$ASDF_PATH' does not exist" >&2
	exit 1
fi

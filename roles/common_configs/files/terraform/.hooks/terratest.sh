#!/bin/bash

# If we're running in a GitHub Action, exit immediately
if [ "$CI" = "true" ]; then
    echo "Running in a GitHub Action, skipping terratest as this is already done by the pre-commit action."
    exit 0
fi

set -e

RETURN_CODE=0

TIMESTAMP=$(date +"%Y%m%d%H%M%S")
LOGFILE="/tmp/terraform-aws-workload-terratest-results-$TIMESTAMP.log"

run_test() {
    repo_root=$(git rev-parse --show-toplevel 2> /dev/null) || exit
    pushd "${repo_root}/test" || exit 1
    echo "Logging output to ${LOGFILE}" | tee -a "$LOGFILE"
    echo "Run the following command to see the output in real time:" | tee -a "$LOGFILE"
    echo "tail -f ${LOGFILE}" | tee -a "$LOGFILE"
    echo "Running tests..." | tee -a "$LOGFILE"

    go test -v -timeout 60m -failfast module_test.go | tee -a "$LOGFILE"
    popd || exit 1
    export RETURN_CODE=$?
}

run_test

if [ $RETURN_CODE -ne 0 ]; then
    echo "Tests failed. Check the log file at ${LOGFILE} for more details." | tee -a "$LOGFILE"
    exit 1
fi

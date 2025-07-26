#!/usr/bin/env bash
set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if docsible is installed
if ! command -v docsible &> /dev/null && ! python3 -m docsible --help &> /dev/null 2>&1; then
    echo -e "${RED}Error: docsible is not installed${NC}"
    echo "Install it with: pip install docsible"
    exit 1
fi

# Function to run docsible
run_docsible() {
    if command -v docsible &> /dev/null; then
        docsible "$@"
    else
        python3 -m docsible "$@"
    fi
}

# Get the repository root
REPO_ROOT=$(git rev-parse --show-toplevel)
cd "$REPO_ROOT"

# Template location
TEMPLATE_PATH=".hooks/templates/docsible-template.md.j2"

# Check if template exists
if [ ! -f "$TEMPLATE_PATH" ]; then
    echo -e "${RED}Error: Template not found at $TEMPLATE_PATH${NC}"
    exit 1
fi

# Track if any files were modified
FILES_MODIFIED=0

# Generate documentation for all roles
if [ -d "roles" ]; then
    echo -e "${YELLOW}Generating documentation for roles...${NC}"

    for role_dir in roles/*/; do
        if [ -d "$role_dir" ]; then
            role_name=$(basename "$role_dir")
            echo -e "Processing role: ${GREEN}$role_name${NC}"

            # Change to the role directory to avoid path issues
            pushd "$role_dir" > /dev/null

            # Generate README for the role
            run_docsible --role . \
                --md-template "$REPO_ROOT/$TEMPLATE_PATH" \
                --output "README.md" \
                --no-backup \
                --no-docsible \
                --comments || {
                    echo -e "  ${RED}Failed to generate documentation for $role_name${NC}"
                    popd > /dev/null
                    continue
            }

            popd > /dev/null

            # Check if the file was modified
            if ! git diff --quiet "${role_dir}README.md" 2> /dev/null; then
                echo -e "  ${YELLOW}Documentation updated - please stage and commit${NC}"
                FILES_MODIFIED=1
            else
                echo "  No changes in documentation"
            fi
        fi
    done
fi

# Generate collection-level documentation if galaxy.yml exists
if [ -f "galaxy.yml" ]; then
    echo -e "${YELLOW}Generating collection documentation...${NC}"

    # For collection-level docs, we might need to use a different approach
    # Try to generate docs for the entire collection
    if run_docsible --collection . \
        --output "README.md" \
        --no-backup \
        --no-docsible 2> /dev/null; then

        # Check if the file was modified
        if ! git diff --quiet "README.md" 2> /dev/null; then
            echo -e "${YELLOW}Collection documentation updated - please stage and commit${NC}"
            FILES_MODIFIED=1
        else
            echo "No changes in collection documentation"
        fi
    else
        echo -e "${YELLOW}Skipping collection-level documentation (not supported or failed)${NC}"
    fi
fi

# Exit with appropriate code
if [ $FILES_MODIFIED -eq 1 ]; then
    echo -e "${YELLOW}Documentation files have been updated${NC}"
    echo -e "${YELLOW}Please review and stage the changes with: git add <files>${NC}"
    echo -e "${YELLOW}Then retry your commit${NC}"
    exit 1  # Exit with failure so the commit doesn't proceed
else
    echo -e "${GREEN}All documentation is up to date${NC}"
    exit 0
fi

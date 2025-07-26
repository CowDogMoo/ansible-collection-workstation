#!/usr/bin/env bash
set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to clean up temporary files on exit
cleanup() {
    # Clean up any temporary files that might have been left behind
    find . -name "*.tmp.before" -o -name "*.tmp.after" | xargs rm -f 2> /dev/null || true
}

# Set up trap to ensure cleanup happens on exit
trap cleanup EXIT INT TERM

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

# Function to preserve custom content outside DOCSIBLE markers
preserve_custom_content() {
    local readme_file="$1"
    local temp_before="${readme_file}.tmp.before"
    local temp_after="${readme_file}.tmp.after"

    # Clean up any existing temp files first
    rm -f "$temp_before" "$temp_after"

    if [ -f "$readme_file" ]; then
        # Check if markers exist
        if grep -q "<!-- DOCSIBLE START -->" "$readme_file" && grep -q "<!-- DOCSIBLE END -->" "$readme_file"; then
            # Extract content before DOCSIBLE START
            sed -n '1,/<!-- DOCSIBLE START -->/p' "$readme_file" | head -n -1 > "$temp_before"

            # Extract content after DOCSIBLE END
            sed -n '/<!-- DOCSIBLE END -->/,$p' "$readme_file" | tail -n +2 > "$temp_after"

            return 0
        fi
    fi

    return 1
}

# Function to merge custom content with docsible output
merge_content() {
    local readme_file="$1"
    local temp_file="${readme_file}.tmp"
    local temp_before="${readme_file}.tmp.before"
    local temp_after="${readme_file}.tmp.after"

    if [ -f "$temp_before" ] || [ -f "$temp_after" ]; then
        # Create new file with preserved content
        if [ -f "$temp_before" ] && [ -s "$temp_before" ]; then
            cat "$temp_before" > "$temp_file"
        fi

        # Add the docsible-generated content
        cat "$readme_file" >> "$temp_file"

        if [ -f "$temp_after" ] && [ -s "$temp_after" ]; then
            cat "$temp_after" >> "$temp_file"
        fi

        # Replace original with merged content
        mv "$temp_file" "$readme_file"
    fi

    # Always clean up temp files after merging
    rm -f "$temp_before" "$temp_after" "$temp_file"
}

# Get the repository root
REPO_ROOT=$(git rev-parse --show-toplevel)
cd "$REPO_ROOT"

# Template locations
ROLE_TEMPLATE_PATH=".hooks/templates/docsible-template.md.j2"
PLAYBOOK_TEMPLATE_PATH=".hooks/templates/playbook-template.md.j2"

# Check if role template exists
if [ ! -f "$ROLE_TEMPLATE_PATH" ]; then
    echo -e "${RED}Error: Role template not found at $ROLE_TEMPLATE_PATH${NC}"
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
            readme_file="${role_dir}README.md"
            echo -e "Processing role: ${GREEN}$role_name${NC}"

            # Preserve custom content if README exists
            has_custom_content=0
            if preserve_custom_content "$readme_file"; then
                has_custom_content=1
            fi

            # Change to the role directory to avoid path issues
            pushd "$role_dir" > /dev/null

            # Generate README for the role
            run_docsible --role . \
                --md-template "$REPO_ROOT/$ROLE_TEMPLATE_PATH" \
                --output "README.md" \
                --no-backup \
                --no-docsible \
                --comments \
                --playbook /dev/null || {
                    echo -e "  ${RED}Failed to generate documentation for $role_name${NC}"
                    popd > /dev/null
                    # Clean up temp files on failure
                    rm -f "${readme_file}.tmp.before" "${readme_file}.tmp.after"
                    continue
            }

            popd > /dev/null

            # Merge custom content if it existed
            if [ $has_custom_content -eq 1 ]; then
                merge_content "$readme_file"
            fi

            # Check if the file was modified
            if ! git diff --quiet "$readme_file" 2> /dev/null; then
                echo -e "  ${YELLOW}Documentation updated - please stage and commit${NC}"
                FILES_MODIFIED=1
            else
                echo "  No changes in documentation"
            fi
        fi
    done
fi

# Generate documentation for playbooks if template exists
if [ -d "playbooks" ] && [ -f "$PLAYBOOK_TEMPLATE_PATH" ]; then
    echo -e "${YELLOW}Generating documentation for playbooks...${NC}"

    for playbook_dir in playbooks/*/; do
        if [ -d "$playbook_dir" ]; then
            playbook_name=$(basename "$playbook_dir")
            playbook_file="${playbook_dir}${playbook_name}.yml"
            readme_file="${playbook_dir}README.md"

            # Check if the main playbook file exists
            if [ -f "$playbook_file" ]; then
                echo -e "Processing playbook: ${GREEN}$playbook_name${NC}"

                # Use jinja2 CLI if available, otherwise use Python
                if command -v jinja2 &> /dev/null; then
                    jinja2 "$PLAYBOOK_TEMPLATE_PATH" \
                        -D playbook_name="$playbook_name" \
                        -D playbook_path="playbooks/$playbook_name" \
                        -D playbook_file="$playbook_name.yml" \
                        > "$readme_file"
                else
                    python3 -c "
import jinja2
import sys
import os

template_path = '$PLAYBOOK_TEMPLATE_PATH'
playbook_name = '$playbook_name'
playbook_path = 'playbooks/$playbook_name'
playbook_file = '$playbook_name.yml'

# Read playbook content
with open('$playbook_file', 'r') as f:
    playbook_content = f.read()

# Load and render template
with open(template_path, 'r') as f:
    template = jinja2.Template(f.read())

output = template.render(
    playbook_name=playbook_name,
    playbook_path=playbook_path,
    playbook_file=playbook_file,
    playbook_content=playbook_content
)

with open('$readme_file', 'w') as f:
    f.write(output)
"
                fi

                # Check if the file was modified
                if ! git diff --quiet "$readme_file" 2> /dev/null; then
                    echo -e "  ${YELLOW}Documentation updated - please stage and commit${NC}"
                    FILES_MODIFIED=1
                else
                    echo "  No changes in documentation"
                fi
            fi
        fi
    done
fi

# Exit with appropriate code
if [ $FILES_MODIFIED -eq 1 ]; then
    echo -e "${YELLOW}Documentation files have been updated${NC}"
    echo -e "${YELLOW}Please review and stage the changes${NC}"
    echo -e "${YELLOW}Then retry your commit${NC}"
    exit 1  # Exit with failure so the commit doesn't proceed
else
    echo -e "${GREEN}All documentation is up to date${NC}"
    exit 0
fi

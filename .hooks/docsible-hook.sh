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

# Template locations
ROLE_TEMPLATE_PATH=".hooks/templates/role-template.md.j2"
PLAYBOOK_TEMPLATE_PATH=".hooks/templates/playbook-template.md.j2"

# Check if role template exists
if [ ! -f "$ROLE_TEMPLATE_PATH" ]; then
    echo -e "${RED}Error: Role template not found at $ROLE_TEMPLATE_PATH${NC}"
    exit 1
fi

# Track if any files were modified
FILES_MODIFIED=0

# Function to update content between DOCSIBLE markers
update_docsible_section() {
    local readme_file="$1"
    local new_content_file="$2"

    if [ -f "$readme_file" ] && grep -q "<!-- DOCSIBLE START -->" "$readme_file" && grep -q "<!-- DOCSIBLE END -->" "$readme_file"; then
        # Create a new README with updated content
        awk '
            /<!-- DOCSIBLE START -->/ {
                print
                print ""
                while ((getline line < "'"$new_content_file"'") > 0) {
                    print line
                }
                close("'"$new_content_file"'")
                print ""
                skip = 1
            }
            /<!-- DOCSIBLE END -->/ {
                print
                skip = 0
                next
            }
            !skip {
                print
            }
        ' "$readme_file" > "${readme_file}.new"

        # Replace the original file
        mv "${readme_file}.new" "$readme_file"
        return 0
    else
        return 1
    fi
}

# Generate documentation for all roles
if [ -d "roles" ]; then
    echo -e "${YELLOW}Generating documentation for roles...${NC}"

    for role_dir in roles/*/; do
        if [ -d "$role_dir" ]; then
            role_name=$(basename "$role_dir")
            readme_file="${role_dir}README.md"
            temp_file="${role_dir}README.md.docsible.tmp"

            echo -e "Processing role: ${GREEN}$role_name${NC}"

            # Generate docsible content to a temporary file
            # Use relative path from repo root and specify output correctly
            if run_docsible --role "$role_dir" \
                --md-template "$ROLE_TEMPLATE_PATH" \
                --output "$temp_file" \
                --no-backup \
                --no-docsible \
                --comments; then

                # Update the README content between DOCSIBLE markers
                if update_docsible_section "$readme_file" "$temp_file"; then
                    echo "  Updated documentation between DOCSIBLE markers"
                else
                    echo -e "  ${YELLOW}No DOCSIBLE markers found, skipping${NC}"
                fi
            else
                echo -e "  ${RED}Failed to generate documentation for $role_name${NC}"
            fi

            # Clean up temp file
            rm -f "$temp_file"

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

# Generate documentation for playbooks using a custom approach
if [ -d "playbooks" ] && [ -f "$PLAYBOOK_TEMPLATE_PATH" ]; then
    echo -e "${YELLOW}Generating documentation for playbooks...${NC}"

    for playbook_dir in playbooks/*/; do
        if [ -d "$playbook_dir" ]; then
            playbook_name=$(basename "$playbook_dir")
            playbook_file="${playbook_dir}${playbook_name}.yml"
            readme_file="${playbook_dir}README.md"
            temp_file="${readme_file}.docsible.tmp"

            # Check if the main playbook file exists
            if [ -f "$playbook_file" ]; then
                echo -e "Processing playbook: ${GREEN}$playbook_name${NC}"

                # Extract playbook information using Python and generate documentation
                if python3 << 'EOF' > "$temp_file"
import yaml
import jinja2
import os
import sys

try:
    # Read playbook content
    with open('${playbook_file}', 'r') as f:
        playbook_content = f.read()
        playbook_data = yaml.safe_load(playbook_content)

    # Extract information from playbook
    playbook_info = {
        'name': '${playbook_name}',
        'path': 'playbooks/${playbook_name}',
        'file': '${playbook_name}.yml',
        'content': playbook_content,
        'plays': []
    }

    # Process plays
    if isinstance(playbook_data, list):
        for play in playbook_data:
            play_info = {
                'name': play.get('name', 'Unnamed play'),
                'hosts': play.get('hosts', 'all'),
                'tasks': []
            }

            # Extract tasks
            tasks = play.get('tasks', [])
            for task in tasks:
                if isinstance(task, dict):
                    task_name = task.get('name', 'Unnamed task')
                    # Get the module name (first key that's not a task directive)
                    module = None
                    task_directives = {
                        'name', 'when', 'with_items', 'loop', 'tags', 'become',
                        'become_user', 'register', 'vars', 'delegate_to', 'run_once',
                        'ignore_errors', 'changed_when', 'failed_when', 'notify',
                        'block', 'rescue', 'always', 'include_role', 'import_role',
                        'include_tasks', 'import_tasks'
                    }
                    for key in task.keys():
                        if key not in task_directives:
                            module = key
                            break

                    play_info['tasks'].append({
                        'name': task_name,
                        'module': module or 'unknown'
                    })

            # Extract roles
            roles = play.get('roles', [])
            play_info['roles'] = []
            for role in roles:
                if isinstance(role, dict):
                    play_info['roles'].append(role.get('role', role.get('name', str(role))))
                else:
                    play_info['roles'].append(str(role))

            # Extract variables
            play_info['vars'] = play.get('vars', {})

            playbook_info['plays'].append(play_info)

    # Load and render template
    with open('${PLAYBOOK_TEMPLATE_PATH}', 'r') as f:
        template = jinja2.Template(f.read())

    output = template.render(
        playbook=playbook_info,
        playbook_name=playbook_info['name'],
        playbook_path=playbook_info['path'],
        playbook_file=playbook_info['file']
    )

    print(output)

except Exception as e:
    print(f"Error processing playbook: {e}", file=sys.stderr)
    sys.exit(1)
EOF
                then
                    # Update the README content between DOCSIBLE markers
                    if update_docsible_section "$readme_file" "$temp_file"; then
                        echo "  Updated documentation between DOCSIBLE markers"
                    else
                        echo -e "  ${YELLOW}No DOCSIBLE markers found, skipping${NC}"
                    fi
                else
                    echo -e "  ${RED}Failed to generate documentation for $playbook_name${NC}"
                fi

                # Clean up temp file
                rm -f "$temp_file"

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

#!/usr/bin/env bash
set -euo pipefail

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Get repo root
REPO_ROOT=$(git rev-parse --show-toplevel)
cd "$REPO_ROOT"

FILES_MODIFIED=0

# Process roles
for role_dir in roles/*/; do
    [ -d "$role_dir" ] || continue

    role_name=$(basename "$role_dir")
    readme="${role_dir}README.md"

    echo "Processing role: $role_name"

    # Save original for comparison
    if [ -f "$readme" ]; then
        cp "$readme" "$readme.bak"
    fi

    # Run docsible - let it do its thing
    cd "$role_dir"
    if docsible --role . --no-docsible --no-backup --comments > /dev/null 2>&1; then
        cd "$REPO_ROOT"

        # Check if changed
        if [ -f "$readme.bak" ]; then
            if ! cmp -s "$readme.bak" "$readme"; then
                echo "  Updated"
                FILES_MODIFIED=1
            else
                echo "  No changes"
            fi
            rm -f "$readme.bak"
        else
            echo "  Created"
            FILES_MODIFIED=1
        fi
    else
        cd "$REPO_ROOT"
        echo "  Failed to generate docs"
        # Restore original if it existed
        if [ -f "$readme.bak" ]; then
            mv "$readme.bak" "$readme"
        fi
    fi
done

# Clean up any docsible backup files
find . -name "README_backup_*.md" -type f -delete 2> /dev/null || true
find . -name ".docsible" -type f -delete 2> /dev/null || true

# Exit
if [ $FILES_MODIFIED -eq 1 ]; then
    echo -e "${YELLOW}Documentation updated. Review and commit.${NC}"
    exit 1
else
    echo -e "${GREEN}All documentation up to date${NC}"
    exit 0
fi

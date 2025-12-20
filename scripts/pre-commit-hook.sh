#!/usr/bin/env bash
#
# Git Pre-commit Hook - Hyprland Wiki
# Runs validation checks before allowing commits
#
# Installation: Copy or symlink to .git/hooks/pre-commit and make executable
#   ln -s ../../scripts/pre-commit-hook.sh .git/hooks/pre-commit
#   chmod +x .git/hooks/pre-commit
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "Running pre-commit validation checks..."
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 not found${NC}"
    echo "Please install Python 3 to run validation checks"
    exit 1
fi

# Track overall success
CHECKS_PASSED=true

# Validate configuration (only if config.toml changed)
if git diff --cached --name-only | grep -q "config.toml"; then
    echo "📋 Validating configuration..."
    if python3 scripts/validate_config.py; then
        echo -e "${GREEN}✓ Configuration validation passed${NC}"
    else
        echo -e "${RED}✗ Configuration validation failed${NC}"
        CHECKS_PASSED=false
    fi
    echo ""
fi

# Validate content (only if markdown files changed)
if git diff --cached --name-only | grep -q "content/.*\.md$"; then
    echo "📝 Validating content..."
    if python3 scripts/validate_content.py; then
        echo -e "${GREEN}✓ Content validation passed${NC}"
    else
        echo -e "${YELLOW}⚠ Content validation found issues (non-blocking)${NC}"
        # Content validation doesn't block commits, just warns
    fi
    echo ""
fi

# Check commit message format (basic check)
COMMIT_MSG_FILE=".git/COMMIT_EDITMSG"
if [ -f "$COMMIT_MSG_FILE" ]; then
    FIRST_LINE=$(head -n1 "$COMMIT_MSG_FILE")
    
    # Check if it follows pattern: "Category/Page: description" or "type: description"
    if [[ ! "$FIRST_LINE" =~ ^[A-Za-z][A-Za-z0-9\ /\-]+:\ .+ ]]; then
        echo -e "${YELLOW}⚠ Commit message format suggestion:${NC}"
        echo "  Preferred: 'Dir/Page: summary' or 'type: summary'"
        echo "  Current:   '$FIRST_LINE'"
        echo ""
    fi
fi

# Final result
if [ "$CHECKS_PASSED" = true ]; then
    echo -e "${GREEN}✓ All pre-commit checks passed${NC}"
    exit 0
else
    echo -e "${RED}✗ Pre-commit checks failed${NC}"
    echo "Fix the issues above or use 'git commit --no-verify' to bypass (not recommended)"
    exit 1
fi

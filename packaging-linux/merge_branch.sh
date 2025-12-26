#!/bin/bash
set -euo pipefail

# Usage: ./merge_branch.sh <branch_name>
# This script fetches the branch, checks it out, shows the diff, and merges it into main if confirmed.

if [ $# -ne 1 ]; then
    echo "Error: Please provide the branch name to merge."
    echo "Usage: ./merge_branch.sh <branch_name>"
    exit 1
fi

BRANCH="$1"
REMOTE_NAME="origin"
MAIN_BRANCH="main"

echo "--- Fetching latest changes ---"
git fetch "$REMOTE_NAME"

echo "--- Checking out the branch ---"
git checkout -b "$BRANCH" "$REMOTE_NAME/$BRANCH"

echo "--- Showing differences from main ---"
git diff "$MAIN_BRANCH"

echo "--- Do you want to merge this branch into $MAIN_BRANCH? (y/n) ---"
read -r response
if [[ "$response" != "y" && "$response" != "Y" ]]; then
    echo "Merge cancelled."
    git checkout "$MAIN_BRANCH"
    exit 0
fi

echo "--- Switching back to $MAIN_BRANCH ---"
git checkout "$MAIN_BRANCH"

echo "--- Merging $BRANCH into $MAIN_BRANCH ---"
git merge "$BRANCH"

echo "--- Pushing the merged changes ---"
git push "$REMOTE_NAME" "$MAIN_BRANCH"

echo "--- Cleaning up local branch ---"
git branch -d "$BRANCH"

echo "Merge completed successfully."
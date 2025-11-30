#!/usr/bin/env bash
set -e
if [ ! -d .git ]; then git init; fi
git add .
git commit -m "Initial commit - LabelForce production starter" || true
if ! command -v gh >/dev/null 2>&1; then
  echo "Please install GitHub CLI (gh): https://cli.github.com/"
  exit 1
fi
gh auth login || true
REPO=labelforce
if ! gh repo view $REPO >/dev/null 2>&1; then
  gh repo create $REPO --public --source=. --remote=origin --push
else
  git push -u origin main || true
fi
echo "Repository pushed. Next: Create services on Render using the render.yaml or via UI."

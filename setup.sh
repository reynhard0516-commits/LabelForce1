#!/usr/bin/env bash
set -e
if [ ! -d .git ]; then git init; fi
git add .
git commit -m "Initial LabelForce A1 starter" || true
if ! command -v gh >/dev/null 2>&1; then echo "Install GH CLI: https://cli.github.com/"; exit 1; fi
gh auth login || true
REPO_NAME="LabelForce1"
if ! gh repo view "$REPO_NAME" >/dev/null 2>&1; then
  gh repo create "$REPO_NAME" --public --source=. --remote=origin --push
else
  git push -u origin HEAD
fi
echo "Pushed. Now open Render and create services or let render.yaml deploy the blueprint."

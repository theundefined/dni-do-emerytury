#!/bin/bash
set -e

# Change to the directory where the script is located
cd "$(dirname "$0")"

# Check if git is clean
if [ -n "$(git status --porcelain)" ]; then
  echo "❌ Error: You have uncommitted changes. Please commit or stash them first."
  exit 1
fi

# Get version from argument
VERSION=$1
if [ -z "$VERSION" ]; then
  echo "Usage: ./release.sh <version>"
  exit 1
fi

# Tag
git tag "v$VERSION"

# Push
echo "🚀 Pushing tag v$VERSION to GitHub..."
git push origin "v$VERSION"

echo "✅ Success! Tag v$VERSION pushed. GitHub Actions will handle the rest."

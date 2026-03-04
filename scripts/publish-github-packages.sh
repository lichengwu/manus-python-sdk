#!/bin/bash
# Manual script to publish to GitHub Packages
# Usage: ./scripts/publish-github-packages.sh

set -e

TOKEN=$(gh auth token)
VERSION=$(python3 -c "import sys; sys.path.insert(0, 'src'); from manus import __version__; print(__version__)")

echo "Publishing manus-sdk v$VERSION to GitHub Packages..."

# Build package
python3 -m build

# Upload to GitHub Packages
twine upload dist/* \
    --repository-url https://pypi.pkg.github.com/lichengwu \
    -u __token__ \
    -p $TOKEN \
    --skip-existing

echo "✓ Published to GitHub Packages!"
echo "Install with: pip install --index-url https://pypi.pkg.github.com/lichengwu/simple manus-sdk"

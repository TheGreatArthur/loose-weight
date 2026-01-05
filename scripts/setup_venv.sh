#!/usr/bin/env bash
set -euo pipefail

# Script pour créer/activer un environnement virtuel et installer les dépendances
# Usage: ./scripts/setup_venv.sh

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "Creating virtual environment at $PROJECT_ROOT/.venv ..."
python3 -m venv .venv

echo "Activating virtual environment..."
# shellcheck source=/dev/null
. .venv/bin/activate

echo "Upgrading pip and installing build tools..."
python -m pip install --upgrade pip setuptools wheel

if [ -f requirements.txt ]; then
  echo "Installing requirements from requirements.txt..."
  python -m pip install -r requirements.txt
else
  echo "No requirements.txt found. You can install Flask with: python -m pip install Flask"
fi

echo "Done. To activate the venv in this shell: source .venv/bin/activate"
echo "To run the app locally:"
echo "  source .venv/bin/activate"
echo "  export FLASK_APP=app.web"
echo "  flask run --reload"

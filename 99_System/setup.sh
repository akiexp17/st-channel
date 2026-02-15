#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "🚀 Setting up st-channel development environment..."

# Python Setup
echo "🐍 Setting up Python environment..."
if [ ! -d "$SCRIPT_DIR/.venv" ]; then
    python3 -m venv "$SCRIPT_DIR/.venv"
    echo "Created virtual environment."
fi

source "$SCRIPT_DIR/.venv/bin/activate"
pip install -r "$PROJECT_ROOT/requirements.txt"
echo "✅ Python dependencies installed."

# Node.js Setup for Quartz
echo "💎 Setting up Quartz..."
if [ -d "$SCRIPT_DIR/quartz" ]; then
    cd "$SCRIPT_DIR/quartz"
    if [ ! -d "node_modules" ]; then
        npm install
        echo "✅ Node modules installed."
    else
        echo "✅ Node modules already installed."
    fi
else
    echo "⚠️ Quartz directory not found in $SCRIPT_DIR/quartz. Skipping Node setup."
fi

echo "🎉 Setup complete! You can now start developing."

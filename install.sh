#!/bin/bash
# 🧹 System Cleanup Master - Quick Install Script

set -e

echo "╔═══════════════════════════════════════════════════════╗"
echo "║        🧹 System Cleanup Master - Installer         ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ This tool is designed for macOS only"
    exit 1
fi

echo "✓ macOS detected"

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    echo "💡 Install Python: brew install python3"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo "✓ Python $PYTHON_VERSION found"

# Create virtual environment
echo ""
echo "📦 Setting up virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install rich click psutil

echo ""
echo "✅ Installation complete!"
echo ""
echo "🚀 Quick Start:"
echo "   make run            # Interactive menu"
echo "   make status         # Check disk usage"
echo "   make help           # Show all commands"
echo ""
echo "📚 Documentation:"
echo "   README.md           # User guide"
echo "   VISUALIZATIONS.md   # Workflow diagrams"
echo "   CLAUDE.md           # AI assistant guide"
echo ""
echo "╔═══════════════════════════════════════════════════════╗"
echo "║              🎉 Ready to clean up!                   ║"
echo "╚═══════════════════════════════════════════════════════╝"

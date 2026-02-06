#!/bin/bash
# Cisco Documentation MCP Server - Setup Script

set -e  # Exit on error

echo "=========================================="
echo "Cisco Documentation MCP Server Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.10 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✓ Found Python $PYTHON_VERSION"
echo ""

# Create virtual environment (optional but recommended)
read -p "Create a virtual environment? (recommended) [y/N]: " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "✓ Virtual environment created and activated"
    echo ""
fi

# Install dependencies
echo "Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Create cisco_docs directory if it doesn't exist
if [ ! -d "cisco_docs" ]; then
    mkdir -p cisco_docs
    echo "✓ Created cisco_docs directory"
else
    echo "✓ cisco_docs directory already exists"
fi
echo ""

# Ask about sample documentation
if [ -z "$(ls -A cisco_docs)" ]; then
    read -p "Create sample Cisco documentation for testing? [y/N]: " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        python3 test_server.py
    fi
fi

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next Steps:"
echo ""
echo "1. Add your Cisco documentation to the cisco_docs/ directory"
echo "   Example: cp ~/Downloads/cisco_manual.pdf cisco_docs/"
echo ""
echo "2. Test the server:"
echo "   python3 test_server.py"
echo ""
echo "3. Choose your server version:"
echo "   - Basic: python3 cisco_docs_mcp_server.py"
echo "   - Advanced: python3 cisco_docs_mcp_server_advanced.py"
echo ""
echo "4. Configure Claude Desktop:"
echo "   See QUICKSTART.md for instructions"
echo ""
echo "Documentation:"
echo "  - README.md - Full documentation"
echo "  - QUICKSTART.md - Quick setup guide"
echo "  - SERVER_COMPARISON.md - Choose basic vs advanced"
echo ""

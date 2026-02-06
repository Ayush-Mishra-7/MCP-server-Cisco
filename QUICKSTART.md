# Quick Start Guide - Cisco Documentation MCP Server

## 5-Minute Setup

### 1. Install Dependencies
```bash
pip install mcp PyPDF2
```

### 2. Test the Server
```bash
# This will create sample documentation and test the server
python test_server.py
```

### 3. Add Your Cisco Documentation
```bash
# Copy your Cisco manuals to the cisco_docs directory
cp ~/Downloads/cisco_router_manual.pdf cisco_docs/
cp ~/Documents/catalyst_guide.txt cisco_docs/switches/
```

### 4. Configure Claude Desktop

**macOS/Linux:**
```bash
# Edit config file
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Windows:**
```powershell
# Edit config file
notepad %APPDATA%\Claude\claude_desktop_config.json
```

**Add this configuration (update paths):**
```json
{
  "mcpServers": {
    "cisco-docs": {
      "command": "python",
      "args": [
        "/full/path/to/cisco_docs_mcp_server.py"
      ]
    }
  }
}
```

### 5. Restart Claude Desktop

### 6. Test It!

In Claude Desktop, try these prompts:
- "What Cisco documentation do we have?"
- "Search for BGP configuration"
- "Read the Cisco 2900 router manual"

## Troubleshooting

**Server not appearing in Claude:**
- Verify Python is in your PATH: `python --version`
- Check the absolute path in the config is correct
- Look for errors in Claude Desktop logs

**Can't read PDF files:**
```bash
pip install --upgrade PyPDF2
# Or try: pip install pdfplumber
```

**Permission denied:**
```bash
chmod +x cisco_docs_mcp_server.py
chmod -R 755 cisco_docs/
```

## Next Steps

See `README.md` for complete documentation and advanced features.

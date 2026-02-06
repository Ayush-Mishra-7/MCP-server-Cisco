# Cisco Documentation MCP Server - Project Overview

## 📁 Project Structure

```
cisco-docs-mcp-server/
├── cisco_docs_mcp_server.py          # Basic MCP server (recommended for starting)
├── cisco_docs_mcp_server_advanced.py # Advanced server with full-text search
├── test_server.py                    # Test script with sample data creation
├── setup.sh                          # Automated setup script
├── requirements.txt                  # Python dependencies
├── pyproject.toml                    # Project metadata
├── .gitignore                        # Git ignore rules
│
├── cisco_docs/                       # Your Cisco documentation goes here
│   └── .gitkeep
│
├── README.md                         # Complete documentation
├── QUICKSTART.md                     # 5-minute setup guide
├── SERVER_COMPARISON.md              # Basic vs Advanced comparison
└── claude_desktop_config.json        # Example Claude Desktop config
```

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)
```bash
./setup.sh
```

### Option 2: Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Test the server
python3 test_server.py

# Run the server
python3 cisco_docs_mcp_server.py
```

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| **README.md** | Complete documentation, all features, troubleshooting |
| **QUICKSTART.md** | Get up and running in 5 minutes |
| **SERVER_COMPARISON.md** | Decide between basic and advanced servers |

## 🔧 Server Files

### Basic Server
- **File:** `cisco_docs_mcp_server.py`
- **Best for:** Small to medium doc sets, getting started
- **Features:** List docs, read docs, simple search

### Advanced Server
- **File:** `cisco_docs_mcp_server_advanced.py`
- **Best for:** Large doc sets, frequent searching
- **Features:** Full-text search, ranking, snippets, indexing

## 🛠 Tools Provided to Claude

When connected, Claude can use these tools:

1. **list_cisco_docs** - List all available documentation
2. **read_cisco_doc** - Read full content of a document
3. **search_cisco_docs** - Search across all documents
4. **summarize_cisco_doc** - Get document summary (advanced only)

## 💡 Example Use Cases

### Network Configuration
```
User to Claude: "Search for BGP configuration examples in our Cisco docs"
Claude: [uses search_cisco_docs tool] → finds relevant configs
```

### Troubleshooting
```
User to Claude: "What does our Cisco 2900 manual say about port configuration?"
Claude: [uses search_cisco_docs then read_cisco_doc] → provides answer
```

### Documentation Discovery
```
User to Claude: "What Cisco switch documentation do we have?"
Claude: [uses list_cisco_docs] → shows all switch-related docs
```

## 🔐 Security Features

- ✅ Path validation prevents directory traversal attacks
- ✅ Only configured directory accessible
- ✅ Read-only access to documents
- ✅ No code execution in documents

## 📊 Supported File Types

- `.txt` - Plain text
- `.md` - Markdown
- `.pdf` - PDF documents (requires PyPDF2)
- `.html` - HTML files
- `.json` - JSON data

## 🎯 Integration Points

### Claude Desktop
Add to `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "cisco-docs": {
      "command": "python",
      "args": ["/path/to/cisco_docs_mcp_server.py"]
    }
  }
}
```

### Custom Applications
Use the MCP protocol to integrate with any LLM application.

## 🧪 Testing

Run the test suite:
```bash
python3 test_server.py
```

Tests include:
- Document listing
- Document reading
- Search functionality
- Security validation

## 📈 Performance Tips

### For Large Document Sets
- Use the advanced server (with indexing)
- Consider organizing docs in subdirectories
- Monitor memory usage during startup

### For Faster Searches
- Use specific search terms
- Organize documents by category
- Use the advanced server's ranked search

## 🔄 Workflow Integration

### As a Full-Stack Developer
```python
# Your Python service can interact with the same docs
from pathlib import Path
import json

# Read configuration docs
config_docs = Path("cisco_docs/config")
for doc in config_docs.glob("*.txt"):
    # Process configuration
    pass
```

### With CI/CD
```yaml
# .github/workflows/validate-docs.yml
- name: Validate Cisco Docs
  run: python3 test_server.py
```

## 🎓 Learning Resources

- [MCP Documentation](https://docs.claude.com) - Official MCP docs
- README.md - This project's full documentation
- test_server.py - Code examples for extending the server

## 🤝 Contributing Ideas

Want to enhance the server? Consider adding:
- Support for `.docx` files
- OCR for scanned PDFs
- Semantic search with embeddings
- Auto-indexing on file changes
- Integration with Cisco DevNet APIs

## 📝 License

MIT License - Use freely for personal or commercial projects

## 🆘 Support

- Check README.md for troubleshooting
- Review test_server.py for examples
- File issues for bugs or feature requests

---

**Ready to start?** Run `./setup.sh` or jump to QUICKSTART.md!

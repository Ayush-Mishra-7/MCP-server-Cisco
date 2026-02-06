# Cisco Documentation MCP Server

A Model Context Protocol (MCP) server that provides LLMs like Claude with access to Cisco router manuals and device documentation.

## Features

- 📚 **Access Cisco Documentation**: Read and search through your Cisco manuals
- 🔍 **Smart Search**: Search by filename or content
- 📄 **Multiple Formats**: Supports TXT, MD, PDF, HTML, and JSON files
- 🔒 **Secure**: Path validation prevents directory traversal attacks
- 🚀 **Easy Integration**: Works with Claude Desktop and other MCP clients

## Installation

### Prerequisites

- Python 3.10 or higher
- pip

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

Or install individually:

```bash
pip install mcp PyPDF2
```

### Step 2: Set Up Your Documentation Directory

Create a directory for your Cisco documentation:

```bash
mkdir -p cisco_docs
```

Add your Cisco manuals to this directory. You can organize them in subdirectories:

```
cisco_docs/
├── routers/
│   ├── cisco_2900_manual.pdf
│   └── cisco_4000_guide.txt
├── switches/
│   ├── catalyst_9300_config.md
│   └── nexus_7000_manual.pdf
└── security/
    └── asa_firewall_guide.pdf
```

## Configuration

### For Claude Desktop

1. **Locate your Claude Desktop config file:**
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%/Claude/claude_desktop_config.json`
   - Linux: `~/.config/Claude/claude_desktop_config.json`

2. **Add the MCP server configuration:**

```json
{
  "mcpServers": {
    "cisco-docs": {
      "command": "python",
      "args": [
        "/absolute/path/to/cisco_docs_mcp_server.py"
      ]
    }
  }
}
```

3. **Restart Claude Desktop**

### For Custom Integration

If you want to configure the documentation directory path, you can modify the `DOCS_DIRECTORY` constant in `cisco_docs_mcp_server.py`:

```python
DOCS_DIRECTORY = Path("/your/custom/path/to/cisco_docs")
```

## Usage

Once configured, the MCP server provides three main tools:

### 1. List All Documentation

Lists all available Cisco documentation files.

**Example prompt to Claude:**
```
List all available Cisco documentation files
```

### 2. Read Specific Document

Reads the complete content of a specific documentation file.

**Example prompt to Claude:**
```
Read the Cisco 2900 router manual
```

### 3. Search Documentation

Searches for documents by keyword in filenames and content.

**Example prompt to Claude:**
```
Search for documentation about BGP routing
```

## Example Queries for Claude

Here are some example questions you can ask Claude when the MCP server is connected:

- "What Cisco router documentation do we have?"
- "Show me the configuration guide for Catalyst switches"
- "Search for information about OSPF in our Cisco docs"
- "Read the ASA firewall manual and summarize the VPN setup process"
- "Find all documentation related to QoS configuration"

## Tools Reference

### `list_cisco_docs`
- **Description**: Lists all available documentation files
- **Parameters**: None
- **Returns**: JSON array of documents with name, path, size, and type

### `read_cisco_doc`
- **Description**: Reads complete content of a specific file
- **Parameters**: 
  - `path` (string, required): Relative path to the document
- **Returns**: Full text content of the document

### `search_cisco_docs`
- **Description**: Searches documentation by keyword
- **Parameters**:
  - `query` (string, required): Search keyword or phrase
- **Returns**: JSON array of matching documents with path and match type

## Advanced Features

### Adding More File Types

To support additional file types, modify the `SUPPORTED_EXTENSIONS` set:

```python
SUPPORTED_EXTENSIONS = {".txt", ".md", ".pdf", ".html", ".json", ".docx", ".xml"}
```

### Custom PDF Parser

For better PDF extraction, consider replacing PyPDF2 with pdfplumber:

```python
def _read_pdf(self, file_path: Path) -> str:
    import pdfplumber
    with pdfplumber.open(file_path) as pdf:
        text = []
        for page in pdf.pages:
            text.append(page.extract_text())
        return "\n".join(text)
```

### Environment Variables

You can configure the server using environment variables by modifying the initialization:

```python
import os
DOCS_DIRECTORY = Path(os.getenv("CISCO_DOCS_PATH", "./cisco_docs"))
```

## Troubleshooting

### Server Not Showing in Claude Desktop

1. Check that the config file path is correct
2. Ensure Python is in your system PATH
3. Verify the absolute path to the server script
4. Check Claude Desktop logs for errors

### PDF Files Not Reading

1. Ensure PyPDF2 is installed: `pip install PyPDF2`
2. For better results, try pdfplumber: `pip install pdfplumber`
3. Some PDFs may be scanned images - consider using OCR

### Permission Errors

Ensure the documentation directory has read permissions:

```bash
chmod -R 755 cisco_docs
```

## Security Considerations

- The server validates all file paths to prevent directory traversal attacks
- Only files within the configured documentation directory are accessible
- Consider running in a restricted environment for production use

## Development

### Running Tests

```bash
pip install pytest pytest-asyncio
pytest
```

### Logging

The server logs to stdout. Adjust logging level in the script:

```python
logging.basicConfig(level=logging.DEBUG)  # More verbose
```

## Contributing

Feel free to extend this server with additional features like:
- Full-text search with ranking
- Document indexing for faster searches
- Version tracking for documentation
- Integration with Cisco API for live data

## License

MIT License - feel free to use and modify for your needs.

## Support

For MCP-related questions, visit the [Anthropic MCP documentation](https://docs.claude.com).

For issues with this server, check the logs and ensure all dependencies are installed correctly.

# Server Comparison Guide

## Which Server Should You Use?

### Basic Server (`cisco_docs_mcp_server.py`)
**Best for:** Getting started quickly, smaller documentation sets

**Features:**
- ✅ Simple setup
- ✅ Fast startup
- ✅ Low memory usage
- ✅ Search by filename and simple content matching
- ✅ Read any document
- ⚠️ Basic search (no ranking)
- ⚠️ Re-reads files on each access

**Use when:**
- You have < 100 documentation files
- You primarily know which documents you need
- You want minimal resource usage
- You're just getting started

### Advanced Server (`cisco_docs_mcp_server_advanced.py`)
**Best for:** Large documentation sets, frequent searching

**Features:**
- ✅ Full-text search with ranking
- ✅ Indexed search (much faster)
- ✅ Snippet extraction showing context
- ✅ Document summaries
- ✅ Word count metadata
- ⚠️ Higher memory usage (keeps index in RAM)
- ⚠️ Slower startup (builds index)

**Use when:**
- You have 100+ documentation files
- You frequently search for specific topics
- You want ranked search results
- You need context snippets in search results

## Performance Comparison

| Feature | Basic | Advanced |
|---------|-------|----------|
| Startup Time | < 1 second | 5-30 seconds (depends on doc count) |
| Memory Usage | ~50MB | ~200MB + (doc size) |
| Search Speed | O(n) - scans all files | O(1) - indexed lookup |
| Search Quality | Exact match only | Ranked by relevance |
| Snippet Preview | No | Yes |

## Migration Path

Start with the **basic server**, then upgrade to **advanced** if you need better search:

```bash
# Step 1: Start with basic
python cisco_docs_mcp_server.py

# Step 2: When you need better search, switch to advanced
# Update your claude_desktop_config.json to point to:
python cisco_docs_mcp_server_advanced.py
```

Both servers use the same `cisco_docs/` directory, so switching is seamless.

## Feature Requests / Future Enhancements

Potential additions for future versions:
- [ ] OCR for scanned PDF documents
- [ ] Semantic search using embeddings
- [ ] Document version tracking
- [ ] Auto-refresh when files change
- [ ] Export search results
- [ ] Integration with Cisco DevNet APIs
- [ ] Support for `.docx` files
- [ ] Fuzzy search (typo tolerance)
- [ ] Multi-language support

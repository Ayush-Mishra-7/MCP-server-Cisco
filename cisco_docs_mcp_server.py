#!/usr/bin/env python3
"""
Cisco Documentation MCP Server
An MCP server that provides access to Cisco router manuals and device documentation
"""

import asyncio
import json
import logging
from pathlib import Path
from typing import Any, Optional
import mcp.types as types
from mcp.server import Server
from mcp.server.stdio import stdio_server
import mcp.server.stdio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cisco-docs-mcp")

# Server instance
app = Server("cisco-docs-mcp")

# Configuration
DOCS_DIRECTORY = Path("./cisco_docs")  # Directory containing your Cisco manuals
SUPPORTED_EXTENSIONS = {".txt", ".md", ".pdf", ".html", ".json"}


class CiscoDocsManager:
    """Manages Cisco documentation files and search"""
    
    def __init__(self, docs_path: Path):
        self.docs_path = docs_path
        self.docs_path.mkdir(exist_ok=True)
        logger.info(f"Initialized Cisco Docs Manager at {self.docs_path}")
    
    def list_documents(self) -> list[dict[str, Any]]:
        """List all available documentation files"""
        docs = []
        if not self.docs_path.exists():
            return docs
        
        for file_path in self.docs_path.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
                docs.append({
                    "name": file_path.name,
                    "path": str(file_path.relative_to(self.docs_path)),
                    "size": file_path.stat().st_size,
                    "type": file_path.suffix
                })
        return docs
    
    def read_document(self, relative_path: str) -> str:
        """Read content from a specific document"""
        file_path = self.docs_path / relative_path
        
        # Security check: ensure path is within docs directory
        try:
            file_path.resolve().relative_to(self.docs_path.resolve())
        except ValueError:
            raise ValueError("Access denied: path outside documentation directory")
        
        if not file_path.exists():
            raise FileNotFoundError(f"Document not found: {relative_path}")
        
        if file_path.suffix.lower() == ".pdf":
            # For PDFs, you'd want to use a library like PyPDF2 or pdfplumber
            return self._read_pdf(file_path)
        else:
            # Read text-based files
            try:
                return file_path.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                return file_path.read_text(encoding='latin-1')
    
    def _read_pdf(self, file_path: Path) -> str:
        """Read PDF content (placeholder - implement based on your needs)"""
        try:
            import PyPDF2
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = []
                for page in pdf_reader.pages:
                    text.append(page.extract_text())
                return "\n".join(text)
        except ImportError:
            return f"[PDF file: {file_path.name}] - Install PyPDF2 to read PDF content"
        except Exception as e:
            return f"[Error reading PDF: {str(e)}]"
    
    def search_documents(self, query: str) -> list[dict[str, Any]]:
        """Search for documents matching a query"""
        results = []
        query_lower = query.lower()
        
        for file_path in self.docs_path.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
                # Search in filename
                if query_lower in file_path.name.lower():
                    results.append({
                        "path": str(file_path.relative_to(self.docs_path)),
                        "name": file_path.name,
                        "match_type": "filename"
                    })
                    continue
                
                # Search in content (for text files)
                if file_path.suffix.lower() in {".txt", ".md", ".html", ".json"}:
                    try:
                        content = file_path.read_text(encoding='utf-8')
                        if query_lower in content.lower():
                            results.append({
                                "path": str(file_path.relative_to(self.docs_path)),
                                "name": file_path.name,
                                "match_type": "content"
                            })
                    except Exception as e:
                        logger.warning(f"Error searching {file_path}: {e}")
        
        return results


# Initialize the docs manager
docs_manager = CiscoDocsManager(DOCS_DIRECTORY)


@app.list_tools()
async def list_tools() -> list[types.Tool]:
    """List available tools for interacting with Cisco documentation"""
    return [
        types.Tool(
            name="list_cisco_docs",
            description="List all available Cisco documentation files in the repository",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        types.Tool(
            name="read_cisco_doc",
            description="Read the complete content of a specific Cisco documentation file",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Relative path to the documentation file"
                    }
                },
                "required": ["path"]
            }
        ),
        types.Tool(
            name="search_cisco_docs",
            description="Search for Cisco documentation files by keyword or phrase",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query (searches filenames and content)"
                    }
                },
                "required": ["query"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[types.TextContent]:
    """Handle tool calls for Cisco documentation operations"""
    
    try:
        if name == "list_cisco_docs":
            docs = docs_manager.list_documents()
            return [types.TextContent(
                type="text",
                text=json.dumps(docs, indent=2)
            )]
        
        elif name == "read_cisco_doc":
            path = arguments.get("path")
            if not path:
                raise ValueError("Missing required argument: path")
            
            content = docs_manager.read_document(path)
            return [types.TextContent(
                type="text",
                text=f"Content of {path}:\n\n{content}"
            )]
        
        elif name == "search_cisco_docs":
            query = arguments.get("query")
            if not query:
                raise ValueError("Missing required argument: query")
            
            results = docs_manager.search_documents(query)
            return [types.TextContent(
                type="text",
                text=json.dumps(results, indent=2)
            )]
        
        else:
            raise ValueError(f"Unknown tool: {name}")
    
    except Exception as e:
        logger.error(f"Error executing tool {name}: {e}")
        return [types.TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]


@app.list_resources()
async def list_resources() -> list[types.Resource]:
    """List available Cisco documentation resources"""
    resources = []
    docs = docs_manager.list_documents()
    
    for doc in docs:
        resources.append(types.Resource(
            uri=f"cisco-doc:///{doc['path']}",
            name=doc['name'],
            mimeType="text/plain",
            description=f"Cisco documentation: {doc['name']}"
        ))
    
    return resources


@app.read_resource()
async def read_resource(uri: str) -> str:
    """Read a specific Cisco documentation resource"""
    if not uri.startswith("cisco-doc:///"):
        raise ValueError(f"Invalid URI scheme: {uri}")
    
    path = uri.replace("cisco-doc:///", "")
    content = docs_manager.read_document(path)
    return content


async def main():
    """Run the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        logger.info("Cisco Documentation MCP Server starting...")
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())

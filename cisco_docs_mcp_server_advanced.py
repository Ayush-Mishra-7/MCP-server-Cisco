#!/usr/bin/env python3
"""
Advanced Cisco Documentation MCP Server with Full-Text Search
Includes document indexing and better search capabilities
"""

import asyncio
import json
import logging
from pathlib import Path
from typing import Any, Optional
import re
from collections import defaultdict
import mcp.types as types
from mcp.server import Server
from mcp.server.stdio import stdio_server

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cisco-docs-mcp-advanced")

app = Server("cisco-docs-mcp-advanced")
DOCS_DIRECTORY = Path("./cisco_docs")
SUPPORTED_EXTENSIONS = {".txt", ".md", ".pdf", ".html", ".json"}


class DocumentIndex:
    """Simple inverted index for full-text search"""
    
    def __init__(self):
        self.index = defaultdict(set)  # word -> set of (doc_path, position)
        self.documents = {}  # doc_path -> content
    
    def tokenize(self, text: str) -> list[str]:
        """Simple tokenization (can be enhanced with NLTK or spaCy)"""
        # Convert to lowercase and split on non-alphanumeric
        words = re.findall(r'\b\w+\b', text.lower())
        return words
    
    def add_document(self, doc_path: str, content: str):
        """Add a document to the index"""
        self.documents[doc_path] = content
        words = self.tokenize(content)
        
        for position, word in enumerate(words):
            self.index[word].add((doc_path, position))
    
    def search(self, query: str, max_results: int = 10) -> list[dict]:
        """Search for documents containing query terms"""
        query_words = self.tokenize(query)
        
        if not query_words:
            return []
        
        # Find documents containing all query words (AND search)
        doc_scores = defaultdict(int)
        
        for word in query_words:
            if word in self.index:
                for doc_path, position in self.index[word]:
                    doc_scores[doc_path] += 1
        
        # Sort by relevance (number of matching terms)
        results = []
        for doc_path, score in sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)[:max_results]:
            # Extract a snippet around the match
            content = self.documents.get(doc_path, "")
            snippet = self._extract_snippet(content, query_words)
            
            results.append({
                "path": doc_path,
                "score": score,
                "snippet": snippet
            })
        
        return results
    
    def _extract_snippet(self, content: str, query_words: list[str], context_chars: int = 150) -> str:
        """Extract a snippet around the first query word match"""
        content_lower = content.lower()
        
        # Find first match position
        min_pos = len(content)
        for word in query_words:
            pos = content_lower.find(word.lower())
            if pos != -1 and pos < min_pos:
                min_pos = pos
        
        if min_pos == len(content):
            return content[:200] + "..." if len(content) > 200 else content
        
        # Extract context around match
        start = max(0, min_pos - context_chars)
        end = min(len(content), min_pos + context_chars)
        
        snippet = content[start:end]
        if start > 0:
            snippet = "..." + snippet
        if end < len(content):
            snippet = snippet + "..."
        
        return snippet


class AdvancedCiscoDocsManager:
    """Advanced manager with indexing and better search"""
    
    def __init__(self, docs_path: Path):
        self.docs_path = docs_path
        self.docs_path.mkdir(exist_ok=True)
        self.index = DocumentIndex()
        self._build_index()
        logger.info(f"Initialized Advanced Cisco Docs Manager with {len(self.index.documents)} documents")
    
    def _build_index(self):
        """Build search index from all documents"""
        logger.info("Building document index...")
        
        if not self.docs_path.exists():
            return
        
        for file_path in self.docs_path.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
                try:
                    relative_path = str(file_path.relative_to(self.docs_path))
                    
                    if file_path.suffix.lower() == ".pdf":
                        content = self._read_pdf(file_path)
                    else:
                        content = file_path.read_text(encoding='utf-8')
                    
                    self.index.add_document(relative_path, content)
                    logger.debug(f"Indexed: {relative_path}")
                    
                except Exception as e:
                    logger.warning(f"Error indexing {file_path}: {e}")
        
        logger.info(f"Index built with {len(self.index.documents)} documents")
    
    def list_documents(self) -> list[dict[str, Any]]:
        """List all indexed documents"""
        docs = []
        for relative_path, content in self.index.documents.items():
            file_path = self.docs_path / relative_path
            docs.append({
                "name": file_path.name,
                "path": relative_path,
                "size": len(content),
                "type": file_path.suffix,
                "word_count": len(self.index.tokenize(content))
            })
        return docs
    
    def read_document(self, relative_path: str) -> str:
        """Read content from indexed document"""
        if relative_path in self.index.documents:
            return self.index.documents[relative_path]
        
        # Fallback to file read if not indexed
        file_path = self.docs_path / relative_path
        
        try:
            file_path.resolve().relative_to(self.docs_path.resolve())
        except ValueError:
            raise ValueError("Access denied: path outside documentation directory")
        
        if not file_path.exists():
            raise FileNotFoundError(f"Document not found: {relative_path}")
        
        if file_path.suffix.lower() == ".pdf":
            return self._read_pdf(file_path)
        else:
            return file_path.read_text(encoding='utf-8')
    
    def _read_pdf(self, file_path: Path) -> str:
        """Read PDF content"""
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
    
    def search_documents(self, query: str, max_results: int = 10) -> list[dict[str, Any]]:
        """Full-text search across all documents"""
        return self.index.search(query, max_results)
    
    def get_document_summary(self, relative_path: str, max_lines: int = 5) -> str:
        """Get a summary of a document (first few lines)"""
        content = self.read_document(relative_path)
        lines = content.split('\n')[:max_lines]
        return '\n'.join(lines)


# Initialize manager
docs_manager = AdvancedCiscoDocsManager(DOCS_DIRECTORY)


@app.list_tools()
async def list_tools() -> list[types.Tool]:
    """List available tools"""
    return [
        types.Tool(
            name="list_cisco_docs",
            description="List all available Cisco documentation files with metadata",
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
            description="Full-text search across all Cisco documentation with ranked results",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query (searches all document content)"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of results to return (default: 10)",
                        "default": 10
                    }
                },
                "required": ["query"]
            }
        ),
        types.Tool(
            name="summarize_cisco_doc",
            description="Get a brief summary (first few lines) of a documentation file",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Relative path to the documentation file"
                    },
                    "max_lines": {
                        "type": "integer",
                        "description": "Maximum number of lines to include (default: 5)",
                        "default": 5
                    }
                },
                "required": ["path"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[types.TextContent]:
    """Handle tool calls"""
    
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
            
            max_results = arguments.get("max_results", 10)
            results = docs_manager.search_documents(query, max_results)
            
            return [types.TextContent(
                type="text",
                text=json.dumps(results, indent=2)
            )]
        
        elif name == "summarize_cisco_doc":
            path = arguments.get("path")
            if not path:
                raise ValueError("Missing required argument: path")
            
            max_lines = arguments.get("max_lines", 5)
            summary = docs_manager.get_document_summary(path, max_lines)
            
            return [types.TextContent(
                type="text",
                text=f"Summary of {path}:\n\n{summary}"
            )]
        
        else:
            raise ValueError(f"Unknown tool: {name}")
    
    except Exception as e:
        logger.error(f"Error executing tool {name}: {e}")
        return [types.TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]


async def main():
    """Run the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        logger.info("Advanced Cisco Documentation MCP Server starting...")
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())

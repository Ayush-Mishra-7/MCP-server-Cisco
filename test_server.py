#!/usr/bin/env python3
"""
Test script for Cisco Documentation MCP Server
Run this to verify your server is working correctly
"""

import asyncio
import json
from pathlib import Path
import sys

# Add the current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from cisco_docs_mcp_server import CiscoDocsManager, DOCS_DIRECTORY


async def test_docs_manager():
    """Test the CiscoDocsManager functionality"""
    
    print("=" * 60)
    print("Testing Cisco Documentation MCP Server")
    print("=" * 60)
    
    # Initialize manager
    manager = CiscoDocsManager(DOCS_DIRECTORY)
    print(f"\n✓ Initialized manager with directory: {DOCS_DIRECTORY}")
    
    # Test 1: List documents
    print("\n--- Test 1: Listing Documents ---")
    docs = manager.list_documents()
    print(f"Found {len(docs)} document(s):")
    for doc in docs:
        print(f"  - {doc['name']} ({doc['size']} bytes, type: {doc['type']})")
    
    if not docs:
        print("\n⚠ Warning: No documents found!")
        print(f"Please add some documentation files to: {DOCS_DIRECTORY}")
        return
    
    # Test 2: Search documents
    print("\n--- Test 2: Searching Documents ---")
    search_query = "cisco"
    results = manager.search_documents(search_query)
    print(f"Search results for '{search_query}': {len(results)} match(es)")
    for result in results:
        print(f"  - {result['name']} (matched in {result['match_type']})")
    
    # Test 3: Read a document
    if docs:
        print("\n--- Test 3: Reading Document ---")
        first_doc = docs[0]
        print(f"Reading: {first_doc['name']}")
        try:
            content = manager.read_document(first_doc['path'])
            preview = content[:200] if len(content) > 200 else content
            print(f"Content preview:\n{preview}")
            if len(content) > 200:
                print(f"... ({len(content)} total characters)")
        except Exception as e:
            print(f"✗ Error reading document: {e}")
    
    # Test 4: Security check - attempt directory traversal
    print("\n--- Test 4: Security Check ---")
    try:
        manager.read_document("../../etc/passwd")
        print("✗ SECURITY ISSUE: Directory traversal not blocked!")
    except ValueError as e:
        print(f"✓ Security check passed: {e}")
    
    print("\n" + "=" * 60)
    print("Testing Complete!")
    print("=" * 60)


def create_sample_docs():
    """Create some sample documentation files for testing"""
    
    DOCS_DIRECTORY.mkdir(exist_ok=True)
    
    sample_docs = {
        "cisco_2900_router.txt": """Cisco 2900 Series Router Configuration Guide
        
Introduction
============
The Cisco 2900 Series Integrated Services Routers (ISR) provide comprehensive 
WAN connectivity, security, and network services.

Key Features:
- Integrated security capabilities
- High-performance routing
- Advanced QoS support
- Multiple WAN interfaces

Basic Configuration:
-------------------
1. Connect to console port
2. Enter privileged EXEC mode: enable
3. Enter global configuration mode: configure terminal
4. Set hostname: hostname Router1
5. Configure interfaces as needed

For detailed configuration examples, refer to the full manual.
""",
        
        "catalyst_9300_switch.md": """# Catalyst 9300 Switch Guide

## Overview
The Catalyst 9300 Series switches are Cisco's flagship enterprise switches.

## Configuration Steps

### Initial Setup
1. Connect console cable
2. Power on the switch
3. Access CLI via terminal

### VLAN Configuration
```
Switch(config)# vlan 10
Switch(config-vlan)# name Engineering
Switch(config-vlan)# exit
```

### Port Configuration
```
Switch(config)# interface GigabitEthernet1/0/1
Switch(config-if)# switchport mode access
Switch(config-if)# switchport access vlan 10
```

## Troubleshooting
- Use `show vlan` to verify VLAN configuration
- Use `show interface status` for port status
""",
        
        "bgp_routing.txt": """BGP Routing Configuration
        
Border Gateway Protocol (BGP) is used for routing between autonomous systems.

Basic BGP Configuration:
router bgp 65001
 bgp log-neighbor-changes
 neighbor 192.168.1.2 remote-as 65002
 network 10.0.0.0 mask 255.255.255.0

Verification Commands:
- show ip bgp summary
- show ip bgp neighbors
- show ip route bgp
"""
    }
    
    for filename, content in sample_docs.items():
        file_path = DOCS_DIRECTORY / filename
        if not file_path.exists():
            file_path.write_text(content)
            print(f"Created sample file: {filename}")


if __name__ == "__main__":
    print("Cisco Documentation MCP Server - Test Suite\n")
    
    # Ask if user wants to create sample docs
    if not any(DOCS_DIRECTORY.iterdir()) if DOCS_DIRECTORY.exists() else True:
        response = input("No documents found. Create sample documentation? (y/n): ")
        if response.lower() == 'y':
            create_sample_docs()
            print()
    
    # Run tests
    asyncio.run(test_docs_manager())

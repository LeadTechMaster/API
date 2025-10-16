#!/usr/bin/env python3
"""
Wrapper script to ensure proper virtual environment usage
"""
import subprocess
import sys
import os

# Get the absolute paths
api_root = "/Users/udishkolnik/API"
venv_python = os.path.join(api_root, ".venv", "bin", "python3")
server_script = os.path.join(api_root, "API_Abilities", "SerpApi", "html", "api_server.py")

# Check if venv python exists
if not os.path.exists(venv_python):
    print(f"❌ Virtual environment Python not found at: {venv_python}")
    print("Please create a virtual environment first:")
    print(f"  cd {api_root}")
    print("  python3 -m venv .venv")
    sys.exit(1)

# Run the server with venv python
print("="*80)
print("🚀 Starting SerpApi Live Data Server with virtual environment")
print("="*80)
print(f"Python: {venv_python}")
print(f"Server: {server_script}")
print("="*80)

os.chdir(os.path.dirname(server_script))
subprocess.run([venv_python, server_script])


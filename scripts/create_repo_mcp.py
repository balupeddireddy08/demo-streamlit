"""Create a GitHub repository via the MCP Server.

Usage:
  setx MCP_TOKEN "<token>"  # Windows persistent; or in powershell: $env:MCP_TOKEN="token" for current session
  python scripts/create_repo_mcp.py --name demo-streamlit --description "MCP Server demo - Stage 1" --public

This script reads MCP server URL from .vscode/mcp.json.
"""
import os
import json
import argparse
from pathlib import Path
import urllib.request
import urllib.error


def load_mcp_url():
    cfg = Path('.vscode/mcp.json')
    if not cfg.exists():
        raise FileNotFoundError(f"{cfg} not found")
    data = json.loads(cfg.read_text())
    return data['servers']['github']['url']


def create_repo(mcp_url, token, name, description, private):
    endpoint = mcp_url.rstrip('/') + '/repos'
    payload = {
        'name': name,
        'description': description,
        'private': bool(private),
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(endpoint, data=data, method='POST')
    req.add_header('Content-Type', 'application/json')
    req.add_header('Authorization', f'Bearer {token}')
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.read().decode('utf-8'), resp.getcode()
    except urllib.error.HTTPError as e:
        return e.read().decode('utf-8'), e.code


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', required=True)
    parser.add_argument('--description', default='')
    parser.add_argument('--public', action='store_true')
    parser.add_argument('--token', default=None, help='MCP token (overrides MCP_TOKEN env)')
    args = parser.parse_args()

    token = args.token or os.environ.get('MCP_TOKEN')
    if not token:
        print('MCP token not provided. Set the MCP_TOKEN environment variable or use --token')
        raise SystemExit(2)

    mcp_url = load_mcp_url()
    body, status = create_repo(mcp_url, token, args.name, args.description, private=(not args.public))
    print('HTTP', status)
    print(body)


if __name__ == '__main__':
    main()

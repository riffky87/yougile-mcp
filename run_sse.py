#!/usr/bin/env python3
"""
SSE transport wrapper for YouGile MCP server.
Used for K8s deployment where stdio transport is not available.
"""

import sys
import os
import asyncio
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# This import registers all tools and loads settings
from src.server import mcp, initialize_auth
from src.config import settings


async def init_auth():
    if (settings.yougile_api_key and settings.yougile_company_id) or \
       (settings.yougile_email and settings.yougile_password and settings.yougile_company_id):
        await initialize_auth()
    else:
        print("[Yougile MCP SSE] WARNING: No authentication credentials provided", file=sys.stderr)


if __name__ == "__main__":
    import uvicorn

    asyncio.run(init_auth())
    port = int(os.environ.get("PORT", "8080"))

    # Disable DNS rebinding protection — in K8s the Host header is the
    # service name (e.g. yougile-mcp:8080), which the SDK rejects by default.
    mcp.settings.transport_security = False

    # Call uvicorn directly instead of mcp.run() to guarantee host/port
    # are respected regardless of MCP SDK version.
    starlette_app = mcp.sse_app()

    print(f"[Yougile MCP SSE] Starting SSE server on 0.0.0.0:{port}", file=sys.stderr)
    uvicorn.run(starlette_app, host="0.0.0.0", port=port)

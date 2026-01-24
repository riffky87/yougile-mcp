"""
Configuration settings for YouGile MCP server.
Manages environment variables and default values.
"""

import os
import sys
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """YouGile MCP server configuration."""
    
    # YouGile API settings
    yougile_base_url: str = "https://yougile.com"
    yougile_email: Optional[str] = None
    yougile_password: Optional[str] = None
    yougile_company_id: Optional[str] = None
    yougile_api_key: Optional[str] = None
    
    # HTTP client settings
    yougile_timeout: int = 30
    yougile_max_retries: int = 3
    yougile_rate_limit_per_minute: int = 50
    
    # MCP server settings
    server_name: str = "YouGile MCP Server"
    server_version: str = "1.0.0"
    
    # User-configurable context instructions (set via MCP client config)
    user_context: Optional[str] = None
    
    # Development settings
    debug: bool = False
    log_level: str = "INFO"
    
    class Config:
        env_prefix = "YOUGILE_"
        env_file = ".env"
        case_sensitive = False


# Find .env file relative to this settings.py file
def find_env_file():
    """Find .env file in project root."""
    current_file = Path(__file__)
    project_root = current_file.parent.parent.parent  # Go up to project root
    env_file = project_root / ".env"
    return str(env_file) if env_file.exists() else None

# Debug: Print ALL environment variables before loading settings
print("[Yougile MCP Settings] DEBUG - ALL environment variables:", file=sys.stderr)
for key, value in sorted(os.environ.items()):
    if 'YOUGILE' in key.upper() or 'API' in key.upper():
        # Mask sensitive values
        display_value = value if 'PASSWORD' not in key.upper() and 'KEY' not in key.upper() else f"***{value[-4:]}" if value else "None"
        print(f"  {key}={display_value}", file=sys.stderr)

# Global settings instance with explicit env file path
env_file_path = find_env_file()
if env_file_path:
    print(f"[Yougile MCP Settings] Loading from env file: {env_file_path}", file=sys.stderr)
    settings = Settings(_env_file=env_file_path)
else:
    print(f"[Yougile MCP Settings] No .env file found, loading from environment", file=sys.stderr)
    settings = Settings()

# Debug: Print loaded settings
print(f"[Yougile MCP Settings] Loaded settings:", file=sys.stderr)
print(f"  yougile_api_key: {'***' + settings.yougile_api_key[-4:] if settings.yougile_api_key else 'None'}", file=sys.stderr)
print(f"  yougile_company_id: {settings.yougile_company_id}", file=sys.stderr)
print(f"  yougile_email: {settings.yougile_email}", file=sys.stderr)

# FALLBACK: Try reading directly from os.environ if pydantic didn't pick it up
if not settings.yougile_api_key and os.environ.get('YOUGILE_API_KEY'):
    print(f"[Yougile MCP Settings] FALLBACK: Reading YOUGILE_API_KEY directly from os.environ", file=sys.stderr)
    settings.yougile_api_key = os.environ.get('YOUGILE_API_KEY')
    
if not settings.yougile_company_id and os.environ.get('YOUGILE_COMPANY_ID'):
    print(f"[Yougile MCP Settings] FALLBACK: Reading YOUGILE_COMPANY_ID directly from os.environ", file=sys.stderr)
    settings.yougile_company_id = os.environ.get('YOUGILE_COMPANY_ID')
    
if not settings.yougile_email and os.environ.get('YOUGILE_EMAIL'):
    print(f"[Yougile MCP Settings] FALLBACK: Reading YOUGILE_EMAIL directly from os.environ", file=sys.stderr)
    settings.yougile_email = os.environ.get('YOUGILE_EMAIL')
    
if not settings.yougile_password and os.environ.get('YOUGILE_PASSWORD'):
    print(f"[Yougile MCP Settings] FALLBACK: Reading YOUGILE_PASSWORD directly from os.environ", file=sys.stderr)
    settings.yougile_password = os.environ.get('YOUGILE_PASSWORD')

print(f"[Yougile MCP Settings] Final settings after fallback:", file=sys.stderr)
print(f"  yougile_api_key: {'***' + settings.yougile_api_key[-4:] if settings.yougile_api_key else 'None'}", file=sys.stderr)
print(f"  yougile_company_id: {settings.yougile_company_id}", file=sys.stderr)
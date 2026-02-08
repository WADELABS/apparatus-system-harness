"""
Security Middleware
===================

Implements Basic Authentication and API Key validation.
"""

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY_NAME = "X-Inquisitor-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def get_api_key(api_key_header: str = Security(api_key_header)):
    """
    Validate API Key from header.
    """
    expected_key = os.getenv("INQUISITOR_API_KEY")
    
    if not expected_key:
        # If no key configured, warn but allow (or fail secure?)
        # Fail secure is better
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server misconfiguration: API Key not set"
        )

    if api_key_header == expected_key:
        return api_key_header
        
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Could not validate credentials"
    )

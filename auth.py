from __future__ import annotations

import os
from typing import Optional

from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def optional_api_key_auth(api_key: Optional[str] = Security(api_key_header)) -> Optional[str]:
    configured_keys = [value.strip() for value in os.getenv("API_KEYS", "").split(",") if value.strip()]
    if not configured_keys:
        return None

    if not api_key or api_key not in configured_keys:
        raise HTTPException(status_code=401, detail="Invalid or missing API key.")

    return api_key

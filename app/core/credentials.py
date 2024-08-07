from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from app.core.config import settings

api_key_header = APIKeyHeader(name="X-API-Key")

def check_api_key(api_key_header: str = Security(api_key_header))-> bool:
    # check api key in env and is Set
    if settings.API_KEY is not None and api_key_header == settings.API_KEY:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Missing or invalid API key"
    )
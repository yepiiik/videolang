from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from services.usage_tracker import usage_tracker

# The client sends the API key in the X-API-Key header
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def verify_api_key(api_key: str = Security(api_key_header)):
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing X-API-Key header",
        )
    
    # In a real app, you would also validate if the api_key exists in Firestore here.
    # For now, we assume it's valid and increment the usage counter.
    usage_tracker.increment_usage(api_key)
    
    return api_key

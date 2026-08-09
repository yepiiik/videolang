from fastapi import APIRouter, Depends
from dependencies.auth import verify_api_key
from services.usage_tracker import usage_tracker
from models.authentication import Authentication

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.get("/usage")
def get_usage(api_key: str = Depends(verify_api_key)):
    """
    Returns the total usage for the provided API key.
    Reads directly from MongoDB.
    """
    total_usage = usage_tracker.get_total_usage(api_key)
    return {
        "api_key": api_key,
        "total_requests": total_usage
    }

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

@router.post("/clear-cache/{uid}")
def clear_cache(uid: str):
    """
    Clears the cached limit for all API keys belonging to the UID in MongoDB.
    This forces a re-fetch of the limit from Firestore on the next request.
    Called by the Next.js frontend when a user upgrades their plan.
    """
    from services.usage_tracker import api_usage_collection
    result = api_usage_collection.update_many(
        {"uid": uid}, 
        {"$unset": {"limit": ""}}
    )
    return {"message": "Cache cleared", "keys_affected": result.modified_count}


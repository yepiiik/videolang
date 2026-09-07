import logging
from fastapi import HTTPException, status
from database.mongodb import database
from database.firestore import get_api_key_limit

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

api_usage_collection = database["api_usage"]

class UsageTracker:
    def increment_usage(self, api_key: str):
        """
        Increments the counter directly in MongoDB ONLY if total_requests < limit.
        If it fails, it checks if the limit is cached. If not, it fetches from Firestore.
        """
        try:
            logger.info(f"Attempting to increment usage for API key: {api_key[:8]}...")
            
            # Atomic update: only increment if total_requests is less than limit
            result = api_usage_collection.update_one(
                {"api_key": api_key, "$expr": {"$lt": ["$total_requests", "$limit"]}},
                {"$inc": {"total_requests": 1}}
            )

            # If modified_count is 1, the request went through perfectly.
            if result.modified_count == 1:
                logger.info(f"Successfully incremented usage for API key: {api_key[:8]}...")
                return

            logger.info(f"Atomic increment failed for API key {api_key[:8]}..., checking limit status.")
            
            # If we get here, either the key doesn't exist, it doesn't have a 'limit' field yet, OR they hit their limit.
            doc = api_usage_collection.find_one({"api_key": api_key})
            
            # Check if cache is missing
            if not doc or "limit" not in doc:
                logger.info(f"Limit cache missing for API key {api_key[:8]}..., fetching from Firestore.")
                # Cache missing: fetch limit from Firestore
                limit, uid = get_api_key_limit(api_key)
                logger.info(f"Fetched limit {limit} for uid {uid}")
                
                # Setup the initial document with the limit
                api_usage_collection.update_one(
                    {"api_key": api_key},
                    {
                        "$set": {"limit": limit, "uid": uid},
                        "$setOnInsert": {"total_requests": 0}
                    },
                    upsert=True
                )
                
                logger.info(f"Limit cached successfully, retrying increment.")
                # Now try again recursively (will either succeed or raise 429 if limit is 0)
                return self.increment_usage(api_key)
                
            # If we get here, the document exists, has a limit, but the atomic update failed.
            # This means total_requests >= limit.
            logger.warning(f"Rate limit exceeded for API key {api_key[:8]}... (Limit: {doc.get('limit')})")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="API rate limit exceeded for your current plan."
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error incrementing usage in MongoDB for key {api_key[:8]}...: {e}")

    def get_total_usage(self, api_key: str) -> int:
        """Retrieves the total usage from MongoDB."""
        try:
            doc = api_usage_collection.find_one({"api_key": api_key})
            if doc:
                return doc.get('total_requests', 0)
        except Exception as e:
            logger.error(f"Error reading usage from MongoDB: {e}")
            
        return 0

usage_tracker = UsageTracker()

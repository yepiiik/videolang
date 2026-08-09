from database.mongodb import database

api_usage_collection = database["api_usage"]

class UsageTracker:
    def increment_usage(self, api_key: str):
        """Increments the counter for a specific API key directly in MongoDB."""
        try:
            api_usage_collection.update_one(
                {"api_key": api_key},
                {"$inc": {"total_requests": 1}},
                upsert=True
            )
        except Exception as e:
            print(f"Error incrementing usage in MongoDB for key {api_key}: {e}")

    def get_total_usage(self, api_key: str) -> int:
        """Retrieves the total usage from MongoDB."""
        try:
            doc = api_usage_collection.find_one({"api_key": api_key})
            if doc:
                return doc.get('total_requests', 0)
        except Exception as e:
            print(f"Error reading usage from MongoDB: {e}")
            
        return 0

usage_tracker = UsageTracker()

import firebase_admin
from firebase_admin import credentials, firestore
from config import FIREBASE_PROJECT_ID, FIREBASE_CLIENT_EMAIL, FIREBASE_PRIVATE_KEY

# Only initialize if credentials are provided
if FIREBASE_PRIVATE_KEY:
    try:
        # Re-format private key correctly since .env might escape newlines
        formatted_private_key = FIREBASE_PRIVATE_KEY.replace('\\n', '\n')
        
        cred = credentials.Certificate({
            "project_id": FIREBASE_PROJECT_ID,
            "private_key": formatted_private_key,
            "client_email": FIREBASE_CLIENT_EMAIL,
        })
        
        # Check if already initialized to avoid duplicate initialization error
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)
            
        db = firestore.client()
    except Exception as e:
        print(f"Failed to initialize Firebase Admin: {e}")
        db = None
else:
    db = None

def get_api_key_limit(api_key: str):
    """
    Searches for the API key in Firestore (users/{uid}/apiKeys).
    Returns a tuple: (limit: int, uid: str)
    If not found, defaults to Free tier limits.
    """
    if db is None:
        return (1000, None)  # Default fallback

    try:
        # Use collection group to find the specific key across all users
        keys_query = db.collection_group('apiKeys').where('key', '==', api_key).limit(1).get()
        
        if not keys_query:
            return (1000, None)
            
        key_doc = keys_query[0]
        # Document path looks like: users/{uid}/apiKeys/{keyId}
        uid = key_doc.reference.parent.parent.id
        
        user_doc = db.collection('users').document(uid).get()
        if not user_doc.exists:
            return (1000, uid)
            
        plan = user_doc.to_dict().get('currentPlan', 'Free')
        
        # Map plans to limits
        limits = {
            'Free': 1000,
            'Pro': 10000,
            'Enterprise': 100000
        }
        
        return (limits.get(plan, 1000), uid)
        
    except Exception as e:
        print(f"Error fetching API key limit from Firestore: {e}")
        return (1000, None)

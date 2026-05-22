import json
import hashlib
import os
from typing import Optional, Any
from app.utils.config import CACHE_DIR

class CacheUtils:
    @staticmethod
    def get_cache_key(query: str, doc_name: Optional[str] = None) -> str:
        """Generates a unique cache key for a query and document selection."""
        base_str = f"{query}_{doc_name or 'all'}"
        return hashlib.md5(base_str.encode()).hexdigest()

    @staticmethod
    def get_from_cache(query: str, doc_name: Optional[str] = None) -> Optional[dict]:
        """Retrieves a cached response if it exists."""
        key = CacheUtils.get_cache_key(query, doc_name)
        cache_file = os.path.join(CACHE_DIR, f"{key}.json")
        if os.path.exists(cache_file):
            with open(cache_file, "r") as f:
                return json.load(f)
        return None

    @staticmethod
    def save_to_cache(query: str, response: dict, doc_name: Optional[str] = None):
        """Saves a response to the cache."""
        key = CacheUtils.get_cache_key(query, doc_name)
        cache_file = os.path.join(CACHE_DIR, f"{key}.json")
        with open(cache_file, "w") as f:
            json.dump(response, f)

import json
import os

CACHE_FILE = "cache.json"


def load_cache():
    if not os.path.exists(CACHE_FILE):
        return {}

    with open(CACHE_FILE, "r") as f:
        return json.load(f)


def save_cache(cache, limit=100):

    if len(cache) > limit:
        keys = list(cache.keys())
        extra = len(keys) - limit

        for i in range(extra):
            del cache[keys[i]]

    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=4)

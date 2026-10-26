
import time

_cache = {}
_hits = 0
_misses = 0


def get_cached(key):
    global _hits, _misses

    entry = _cache.get(key)

    if entry is not None:
        if time.time() < entry["expires_at"]:
            _hits += 1
            return entry["result"].copy()

        del _cache[key]

    _misses += 1
    return None


def store_cached(key, result, ttl):
    if ttl is None or ttl <= 0:
        return

    _cache[key] = {
        "result": result.copy(),
        "expires_at": time.time() + ttl
    }


def get_cache_stats():
    total = _hits + _misses
    hit_ratio = (_hits / total * 100) if total else 0

    return {
        "hits": _hits,
        "misses": _misses,
        "hit_ratio": round(hit_ratio, 2),
        "total_queries": total,
        "cached_entries": len(_cache)
    }


def clear_cache():
    global _hits, _misses

    _cache.clear()
    _hits = 0
    _misses = 0

    return {
        "message": "DNS cache cleared successfully",
        "hits": 0,
        "misses": 0,
        "hit_ratio": 0,
        "total_queries": 0,
        "cached_entries": 0
    }

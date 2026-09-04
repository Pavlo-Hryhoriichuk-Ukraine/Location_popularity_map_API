from django.core.cache import cache

LOCATION_LIST_VERSION_KEY = 'locations:list:version'
LOCATION_LIST_TIMEOUT = 300


def get_location_list_cache_key(query_string: str) -> str:
    version = cache.get(LOCATION_LIST_VERSION_KEY)
    if version is None:
        cache.add(LOCATION_LIST_VERSION_KEY, 1, timeout=None)
        version = cache.get(LOCATION_LIST_VERSION_KEY, 1)
    return f'locations:list:v{version}:{query_string}'


def invalidate_location_list_cache() -> None:
    if not cache.add(LOCATION_LIST_VERSION_KEY, 1, timeout=None):
        cache.incr(LOCATION_LIST_VERSION_KEY)

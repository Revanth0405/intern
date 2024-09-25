from file import MultiLevelCache
if __name__ == "__main__":
    # Initialize multi-level cache system
    ml_cache = MultiLevelCache()

    # Add cache levels with different eviction policies
    ml_cache.add_cache_level(3, 'LRU')  # L1 with size 3, LRU eviction
    ml_cache.add_cache_level(2, 'LFU')  # L2 with size 2, LFU eviction

    # Insert key-value pairs into the cache
    ml_cache.put("A", "1")
    ml_cache.put("B", "2")
    ml_cache.put("C", "3")

    # Retrieve value to ensure L1 cache hit
    ml_cache.get("A")  # This should return "1" from L1

    # Insert a new value that causes eviction in L1 (LRU policy)
    ml_cache.put("D", "4")

    # Fetch C from L2 and promote to L1
    ml_cache.get("C")

    # Display current state of caches
    ml_cache.display_cache()

### Here is the github link --- https://github.com/Revanth0405/intern

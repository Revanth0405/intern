from collections import OrderedDict, defaultdict

class CacheLevel:
    def __init__(self, size, eviction_policy):
        self.size = size
        self.eviction_policy = eviction_policy
        if eviction_policy == 'LRU':
            self.cache = OrderedDict()  # LRU cache uses OrderedDict
        elif eviction_policy == 'LFU':
            self.cache = {}
            self.freq = defaultdict(int)  # LFU cache tracks frequencies

    def get(self, key):
        """ Retrieves a value from the cache and updates its status """
        if key in self.cache:
            if self.eviction_policy == 'LRU':
                self.cache.move_to_end(key)  # LRU: Update usage order
            elif self.eviction_policy == 'LFU':
                self.freq[key] += 1  # LFU: Increase access frequency
            return self.cache[key]
        return None

    def put(self, key, value):
        """ Inserts a key-value pair, handling eviction if necessary """
        if key in self.cache:
            if self.eviction_policy == 'LRU':
                self.cache.move_to_end(key)  # LRU: Update usage order
            elif self.eviction_policy == 'LFU':
                self.freq[key] += 1  # LFU: Increase access frequency
        elif len(self.cache) >= self.size:
            self.evict()  # Evict an entry if the cache is full
        self.cache[key] = value
        if self.eviction_policy == 'LFU':
            self.freq[key] = 1

    def evict(self):
        """ Evicts an entry based on the chosen eviction policy """
        if self.eviction_policy == 'LRU':
            self.cache.popitem(last=False)  # LRU eviction: Remove least recent
        elif self.eviction_policy == 'LFU':
            lfu_key = min(self.freq, key=self.freq.get)  # LFU eviction: Remove least frequent
            del self.cache[lfu_key]
            del self.freq[lfu_key]

    def display(self):
        """ Returns a formatted string of the current cache state """
        return [f"{k}: {v}" for k, v in self.cache.items()]

class MultiLevelCache:
    def __init__(self):
        self.cache_levels = []

    def add_cache_level(self, size, eviction_policy):
        """ Adds a new cache level to the system """
        new_cache = CacheLevel(size, eviction_policy)
        self.cache_levels.append(new_cache)
        print(f"Cache level added with size {size} and eviction policy {eviction_policy}.")

    def remove_cache_level(self, level):
        """ Removes a cache level at the specified index """
        if 0 <= level < len(self.cache_levels):
            self.cache_levels.pop(level)
            print(f"Cache level {level + 1} removed.")
        else:
            print("Invalid cache level.")

    def get(self, key):
        """ Retrieves data across cache levels """
        for i, cache in enumerate(self.cache_levels):
            value = cache.get(key)
            if value:
                print(f"Cache hit at level {i + 1} for key '{key}'.")
                self.promote(key, value, i)
                return value
        print(f"Cache miss for key '{key}'.")
        return None

    def put(self, key, value):
        """ Inserts data into the highest-priority (L1) cache """
        if self.cache_levels:
            print(f"Inserting key '{key}' with value '{value}' into L1 cache.")
            self.cache_levels[0].put(key, value)

    def promote(self, key, value, from_level):
        """ Promotes data from a lower cache to higher levels """
        for i in range(from_level, 0, -1):
            self.cache_levels[i].cache.pop(key, None)  # Remove from lower level
            self.cache_levels[i - 1].put(key, value)  # Insert into the higher level

    def display_cache(self):
        """ Displays the contents of each cache level """
        for i, cache in enumerate(self.cache_levels):
            print(f"L{i + 1} Cache: {cache.display()}")

### Here is the github link --- https://github.com/Revanth0405/intern

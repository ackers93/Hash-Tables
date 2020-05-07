class HashTableEntry:
    """
    Hash Table entry, as a linked list node.
    """

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class HashTable:
    """
    A hash table that with `capacity` buckets
    that accepts string keys

    Implement this.
    """

    def __init__(self, capacity):
        self.capacity = capacity
        self.storage = [None] * capacity
        self.elements = 0

    def fnv1(self, key):
        """
        FNV-1 64-bit hash function

        Implement this, and/or DJB2.
        """
        hash_value = 15747584280476905290
        for x in key:
            hash_value = hash_value * 45110794018066056677
            hash_value = hash_value ^ ord(x)
        return hash_value

    def djb2(self, key):
        """
        DJB2 32-bit hash function

        Implement this, and/or FNV-1.
        """
        hash = 4587
        for c in key:
            hash = (hash * 33) + ord(c)
        return hash & 0xffffffff

    def hash_index(self, key):
        """
        Take an arbitrary key and return a valid integer index
        between within the storage capacity of the hash table.
        """
        # return self.fnv1(key) % self.capacity
        return self.djb2(key) % self.capacity

    def load_factor(self):
        # Load Factor is number of elements in a list divided by the number of slots (capacity)
        return self.elements/self.capacity

    def put(self, key, value):
        """
        Store the value with the given key.

        Hash collisions should be handled with Linked List Chaining.

        Implement this.
        """
        # find index based on key passed in
        index = self.hash_index(key)
        # check storage with index from above
        existing_entry = self.storage[index]

        new_entry = HashTableEntry(key, value)

        # check to see if hash index exists
        if existing_entry:
            last_entry = None
            # Look through hash index list
            while existing_entry:
                # search list for key
                if existing_entry.key == key:
                    # if existing key is found, replace it
                    existing_entry.value = value
                    return
                # continue looking through list until None
                last_entry = existing_entry
                existing_entry = existing_entry.next
            # if the existing entry is not found, add to the end of hash index list.
            last_entry.next = new_entry
            self.elements += 1
            # automatically resize by double if load facto is greater than 0.7
            if self.load_factor() > 0.7:
                self.resize(self.capacity * 2)

        # If hash index doesn't exist, add new entry in that spot
        else:
            self.storage[index] = new_entry
            self.elements += 1
            # automatically resize by double if load facto is greater than 0.7
            if self.load_factor() > 0.7:
                self.resize(self.capacity * 2)

    def delete(self, key):
        """
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        Implement this.
        """
        # find index based on key passed in
        index = self.hash_index(key)
        # check storage with index
        existing_entry = self.storage[index]

        # check to see if hash index exists:
        if existing_entry:
            last_entry = None
            # look through this hash index list
            while existing_entry:
                # search list for key
                if existing_entry.key == key:
                    # if it matches the key, set the last entry's next in list to the next index
                    # deletes but moves the following up
                    if last_entry:
                        last_entry.next = existing_entry.next
                    else:
                        # if nothing else in list, set the next hash index to current spot
                        self.storage[index] = existing_entry.next
                    # continue looking through list until None
                    last_entry = existing_entry
                    existing_entry = existing_entry.next
        else:
            # key is found, print warning
            print('no key found')

    def get(self, key):
        """
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        Implement this.
        """
        # find index based on key being passed in
        index = self.hash_index(key)
        # check storage with above index
        existing_entry = self.storage[index]

        # check to see if that hash index exists
        if existing_entry:
            # look through this hash index list
            while existing_entry:
                # search list for key
                if existing_entry.key == key:
                    # if found, return value
                    return existing_entry.value
                    # continue looking through list until None
                existing_entry = existing_entry.next
        else:
            # key is not found, return None
            return None

    def resize(self, new_capacity):
        """
        Doubles the capacity of the hash table and
        rehash all key/value pairs.

        Implement this.
        """
        prev_storage = self.storage

        # Step 1: make a new, bigger table/array
        # ....Update capacity on new capacity
        # ....Update storage with new capacity

        self.capacity = new_capacity
        self.storage = [None] * new_capacity

        # Step 2: go through all the old elements, and hash into the new list
        # Look through each key value pair in previous storage
        for i in range(len(prev_storage)):
            # Check previous storage with i as index
            existing_entry = prev_storage[i]

            # Check to see if that hash index exists:
            if existing_entry:
                # Look through this hash index list
                while existing_entry:
                    if existing_entry.key:
                        # If found, rehash to new storage
                        self.put(existing_entry.key, existing_entry.value)
                    # Continue looking through list until None
                    existing_entry = existing_entry.next


if __name__ == "__main__":
    ht = HashTable(2)

    ht.put("line_1", "Tiny hash table")
    ht.put("line_2", "Filled beyond capacity")
    ht.put("line_3", "Linked list saves the day!")

    print("")

    # Test storing beyond capacity
    print(ht.get("line_1"))
    print(ht.get("line_2"))
    print(ht.get("line_3"))

    # Test resizing
    old_capacity = len(ht.storage)
    ht.resize(1024)
    new_capacity = len(ht.storage)

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

   # Test if data intact after resizing
    print(ht.get("line_1"))
    print(ht.get("line_2"))
    print(ht.get("line_3"))

    print("")

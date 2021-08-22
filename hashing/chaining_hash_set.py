from chaining_hash_node import Chaining_Hash_Node

class Chaining_Hash_Set():

    def __init__(self, capacity = 0):
        self.hash_table = [None] * capacity
        self.table_size = 0

    def get_hash_code(self, key, hash_table_length):
        """Hash function that calculates a hash code for a given key using the modulo division.
        @param key:
        		Key for which a hash code shall be calculated according to the length of the hash table.
        @param hash_table_length:
        		Length of the hash table.
        @return:
        		The calculated hash code for the given key.
        """
        hash_code = key % hash_table_length
        return hash_code

    def get_hash_table(self):
        """(Required for testing only)
        @return the hash table.
        """
        return self.hash_table

    def set_hash_table(self, table, size):
        """(Required for testing only) Set a given hash table which shall be used.
        @param table:
        		Given hash table which shall be used.
        @param size:
        		Number of already stored keys in the given table.
        """
        self.hash_table = table
        self.table_size = size

    def get_table_size(self):
        """returns the number of stored keys (keys must be unique!).
    	 """
        return self.table_size

    def insert(self, key, data):
        """Inserts a key and returns true if it was successful. If there is already an entry with the
          same key or the hash table is full, the new key will not be inserted and false is returned.

         @param key:
         		The key which shall be stored in the hash table.
         @param data:
         		Any data object that shall be stored together with a key in the hash table.
         @return:
         		true if key could be inserted, or false if the key is already in the hash table.
         @throws:
         		a ValueError exception if any of the input parameters is None.
         """
        if key is None or data is None:
            return ValueError("Some of the input parameters is None")

        #Getting the length of the hash_table and the hash_code
        hash_table_length = len(self.hash_table)
        hash_code = self.get_hash_code(key, hash_table_length)

        #If there is no entry, a new node is inserted:
        if self.hash_table[hash_code] is None:
            self.hash_table[hash_code] = Chaining_Hash_Node(key, data)
            self.table_size += 1
            return True
        #If there is an entry:
        else:
            #The first node in the entry is set as cur_node
            cur_node = self.hash_table[hash_code]
            #Checking if the existing node has the same key as the key being inserted
            if cur_node.key == key:
                return False
            #Finding the node with no next node, while also checking for a duplicate key
            while cur_node.next:
                if cur_node.next.key == key:
                    return False
                cur_node = cur_node.next
            #Adding the last node in the entry with the key and data to be inserted
            cur_node.next = Chaining_Hash_Node(key,data)
            self.table_size += 1
            return True


    def contains(self, key):
        """Searches for a given key in the hash table.
         @param key:
         	    The key to be searched in the hash table.
         @return:
         	    true if the key is already stored, otherwise false.
         @throws:
         	    a ValueError exception if the key is None.
         """
        if key is None:
            return ValueError("The key is None")

        # Getting the length of the hash_table and the hash_code
        hash_table_length = len(self.hash_table)
        hash_code = self.get_hash_code(key, hash_table_length)

        #If the corresponding slot is empty, return False
        if self.hash_table[hash_code] is None:
            return False
        #Otherwise check every node in the entry
        else:
            cur_node = self.hash_table[hash_code]
            while cur_node:
                if cur_node.key == key:
                    return True
                cur_node = cur_node.next
            return False


    def remove(self, key):
        """Removes the key from the hash table and returns true on success, false otherwise.
        @param key:
        		The key to be removed from the hash table.
        @return:
        		true if the key was found and removed, false otherwise.
        @throws:
         	a ValueError exception if the key is None.
        """
        if key is None:
            return ValueError("The key is None")

        # Getting the length of the hash_table and the hash_code
        hash_table_length = len(self.hash_table)
        hash_code = self.get_hash_code(key, hash_table_length)

        #If the corresponding slot is empty, return False
        if self.hash_table[hash_code] is None:
            return False
        #Otherwise check every node in the entry
        else:
            #Setting cur_node, next_node, next_next_node to connect the nodes before and after a deleted node if necessary
            cur_node = self.hash_table[hash_code]
            next_node = cur_node.next
            if next_node:
                next_next_node = next_node.next

            #If the first node in the entry has the node to be removed...
            if cur_node.key == key:
                #...and it is the only node in the entry, the slot is set to None
                if cur_node.next is None:
                    self.hash_table[hash_code] = None
                    self.table_size -= 1
                    return True
                #Otherwise the slot in the table is set to the next node of the current node
                else:
                    self.hash_table[hash_code] = cur_node.next
                    self.table_size -= 1
                    return True
            else:
                #Otherwise checking each node one by one till the end of the chain
                while next_node:
                    #If the node to be removed is not the last one in the chain
                    if next_node.key == key:
                        if next_next_node:
                            #The next node of the node before the node to remove is set to the next node of the node to remove
                            cur_node.next =next_next_node
                            self.table_size -= 1
                            return True
                        #If the node to remove is the last one in the chain, the next node of the node before
                        #the node to be removed is set to None
                        else:
                            cur_node.next = None
                            self.table_size -= 1
                            return True
                    cur_node = cur_node.next
                    next_node = cur_node.next
                    if next_node:
                        next_next_node = next_node.next
            return False

    def clear(self):
        """Removes all stored elements from the hash table by setting all nodes to None.
        """
        for i in range(len(self.hash_table)):
            self.hash_table[i] = None
        self.table_size = 0

from open_hash_node import Open_Hash_Node

class Double_Hash_Set():

    def __init__(self, capacity = 0):
        self.hash_table = [None] * capacity
        self.table_size = 0

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

    def get_hash_code_2(self, key, hash_table_length):
        """Hash function 2 for double hashing, that calculates a key specific offset.
        @param key:
        		Key for which a hash code shall be calculated according to the length of the hash table.
        @param hash_table_length:
        		Length of the hash table.
        @return:
        		The calculated hash code for the given key.
        """
        hash_code_2 = 1+(key % (hash_table_length-1))
        return hash_code_2

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
        #If the hash_table is full
        if len(self.hash_table) == self.table_size:
            return False

        #Getting hash_code_1 and adding a new node in the corresponding slot in the table if it is empty or
        #the node has been previously removed
        hash_code_1 = key % len(self.hash_table)
        if self.hash_table[hash_code_1] == None or self.hash_table[hash_code_1].removed == True:
            self.hash_table[hash_code_1] = Open_Hash_Node(key,data)
            self.table_size += 1
            return True
        else:
            #If the node with the same key is already in the slot
            if self.hash_table[hash_code_1].key == key and self.hash_table[hash_code_1].removed == False:
                return False
            else:
                #Otherwise searching for an empty slot using hash_code_1 and hash_code_2
                old_hash_value = hash_code_1
                new_hash_value = (old_hash_value + self.get_hash_code_2(key,len(self.hash_table))) % len(self.hash_table)
                while new_hash_value >=0:
                    #If the key with the same key as the one to be inserted already exists
                    if self.hash_table[new_hash_value].key == key and self.hash_table[new_hash_value].removed == False:
                        return False
                    #Adding a new node in the corresponding slot in the table if it is empty or
                    #the node has been previously removed
                    elif self.hash_table[new_hash_value] == None or self.hash_table[new_hash_value].removed == True:
                        self.hash_table[new_hash_value] = Open_Hash_Node(key, data)
                        self.table_size += 1
                        return True
                    else:
                        new_hash_value = (new_hash_value + self.get_hash_code_2(key, len(self.hash_table))) % len(
                            self.hash_table)


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

        #Getting hash_code_1 and checking if the key of the node in the corresponding table slot is the one
        #that needs to be found
        hash_code_1 = key % len(self.hash_table)
        if self.hash_table[hash_code_1] == None:
            return False
        if self.hash_table[hash_code_1].key == key:
            return True
        #Otherwise searching for next slots using hash_code_1 and hash_code_2 till the element is found or
        #an initially empty slot is found or the whole table has been traversed.
        old_hash_value = hash_code_1
        new_hash_value = (old_hash_value + self.get_hash_code_2(key, len(self.hash_table))) % len(self.hash_table)
        #Creating a set to keep track of the visited slots in the hash_table
        traversed_hash_values = set()
        traversed_hash_values.add(old_hash_value)
        while new_hash_value >= 0:
            #If the node is initially None
            if self.hash_table[new_hash_value] == None:
                return False
            #If the slot has been already visited
            elif len(traversed_hash_values) > len(self.hash_table) or new_hash_value in traversed_hash_values:
                return False
            #If the searched for key is found
            elif self.hash_table[new_hash_value].key == key:
                return True
            else:
                traversed_hash_values.add(new_hash_value)
                new_hash_value = (new_hash_value + self.get_hash_code_2(key, len(self.hash_table))) % len(
                self.hash_table)



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

        # Getting hash_code_1 and checking if the key of the node in the corresponding table slot is the one
        # that needs to be removed
        hash_code_1 = key % len(self.hash_table)
        if self.hash_table[hash_code_1] == None:
            return False
        if self.hash_table[hash_code_1].key == key:
            #If yes, setting the node to (None,None,True)
            self.hash_table[hash_code_1] = Open_Hash_Node(None, None, True)
            self.table_size -= 1
            return True
        # Otherwise searching for next slots using hash_code_1 and hash_code_2 till the element is found or
        # an initially empty slot is found or the whole table has been traversed.
        old_hash_value = hash_code_1
        new_hash_value = (old_hash_value + self.get_hash_code_2(key, len(self.hash_table))) % len(self.hash_table)
        # Creating a set to keep track of the visited slots in the hash_table
        traversed_hash_values = set()
        traversed_hash_values.add(old_hash_value)
        while new_hash_value >= 0:
            # If the node is initially None
            if self.hash_table[new_hash_value] == None:
                return False
            #If the slot has been already visited
            elif len(traversed_hash_values) > len(self.hash_table) or new_hash_value in traversed_hash_values:
                return False
            #If the searched for key is found, setting the node to (None,None,True)
            elif self.hash_table[new_hash_value].key == key:
                self.hash_table[new_hash_value] = Open_Hash_Node(None, None, True)
                self.table_size -= 1
                return True
            else:
                traversed_hash_values.add(new_hash_value)
                new_hash_value = (new_hash_value + self.get_hash_code_2(key, len(self.hash_table))) % len(
                self.hash_table)

    def clear(self):
        """Removes all stored elements from the hash table by setting all nodes to None.
        """
        for i in range(len(self.hash_table)):
            self.hash_table[i] = None
        self.table_size = 0

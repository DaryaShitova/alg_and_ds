from avl_node import AVLNode


class AVLTree:

    def __init__(self):
        """Default constructor. Initializes the AVL tree.
        """
        self.root = None
        self.size = 0

    def get_root(self):
        """@returns the root of the AVLTree
        """
        return self.root

    def get_height(self):
        """Retrieves tree height.
    	 @return -1 in case of empty tree, current tree height otherwise.
    	 """
        if self.root is None:
            return -1
        else:
            return self.root.height

    def get_size(self):
        """Yields number of key/element pairs in the tree.
        @return Number of key/element pairs.
        """
        return self.size

    def to_array(self):
        """Yields an array representation of the tree elements (pre-order).
    	@return Array representation of the tree elements.
        """
        if self.root:
            curr_node = self.root
        else:
            return None
        array = []
        result = self.to_array_helper(curr_node, array)
        return result

    def find(self, key):
        """Returns element of node with given key.
    	 @param key: Key to search.
    	 @return Corresponding element if key was found, None otherwise.
         @raises ValueError if the key is None
    	 """
        if key is None:
            raise ValueError("Key must not be None")

        if self.root:
            result = self._find_helper(key,
                                       self.root)  # A helper function to iterate over the BST till the key is found.
            if result:
                return result.elem
            else:
                return None
        else:
            return None

    def insert(self, key, elem):
        """Inserts a new node into AVL tree.
    	 @param key: Key of the new node.
    	 @param elem: Data of the new node. Elements with the same key
    	 are not allowed. In this case false is returned. None-Keys are
    	 not allowed. In this case an exception is thrown.
         @raises ValueError if the key or elem is None.
        """
        if key is None or elem is None:
            raise ValueError("Either key or elem is None")

        #If the key already in the tree - return False
        if self.find(key):
            return False
        new_node = AVLNode(key, elem)
        #If the tree is empty, the new_node will be the root
        if self.root is None:
            self.root = new_node
        #Otherwise use the helper function for insertion:
        else:
            self._insert_helper(self.root, new_node)
        self.size += 1
        return True

    def remove(self, key):
        """Removes node with given key.
    	 @param key: Key of node to remove.
    	 @return true If element was found and deleted.
         @raises ValueError if the key is None
        """
        if key is None:
            raise ValueError("Key must not be None")

        #If the tree is empty, there is nothing to remove
        if self.root is None:
            return False

        #If the node to remove is not in the tree - return False
        if self._find_helper(key, self.root) is None:
            return False

        # Use regular binary tree removal and return the sucessor of the node to remove
        successor = self._remove_helper(key)

        while successor:
            successor.height = 1 + max(self.get_depth(successor.left), self.get_depth(successor.right))
            bl = self.get_balance(successor)
            if bl > 1:
                z = successor
                y = z.left
                if self.get_balance(z.left) >= 0:
                    x = y.left
                    T2 = y.right

                    # Restructuring
                    if self.get_root() == z:
                        self.root = y
                        y.parent = None
                    else:
                        if z.parent.left == z:
                            z.parent.left = y
                        if z.parent.right == z:
                            z.parent.right = y
                        y.parent = z.parent

                    y.right = z
                    z.parent = y

                    if T2:
                        z.left = T2
                        T2.parent = z
                    else:
                        z.left = None

                    # Updating the heights of the nodes
                    x.height = 1 + max(self.get_depth(x.left), self.get_depth(x.right))
                    z.height = 1 + max(self.get_depth(z.left), self.get_depth(z.right))
                    y.height = 1 + max(self.get_depth(y.left), self.get_depth(y.right))

                else:
                    x = y.right
                    T1 = x.left
                    T2 = x.right

                    # Restructuring
                    if self.get_root() == z:
                        self.root = x
                        x.parent = None
                    else:
                        if z.parent.right == z:
                            z.parent.right = x
                        if z.parent.left == z:
                            z.parent.left = x
                        x.parent = z.parent

                    x.left = y
                    y.parent = x
                    if T1:
                        y.right = T1
                        T1.parent = y
                    else:
                        y.right = None
                    x.right = z
                    z.parent = x
                    if T2:
                        z.left = T2
                        T2.parent = z
                    else:
                        z.left = None

                    # Updating the heights of the nodes
                    y.height = 1 + max(self.get_depth(y.left), self.get_depth(y.right))
                    z.height = 1 + max(self.get_depth(z.left), self.get_depth(z.right))
                    x.height = 1 + max(self.get_depth(x.left), self.get_depth(x.right))

            if bl < -1:
                z = successor
                y = z.right
                if self.get_balance(z.left) >= 0:
                    x = y.left
                    if x:
                        T1 = x.left
                        T2 = x.right
                        if T1:
                            z.right = T1
                            T1.parent = z
                        else:
                            z.right = None
                        if T2:
                            y.left = T2
                            T2.parent = y
                        else:
                            y.left = None

                    # Restructuring
                    if self.get_root() == z:
                        self.root = x
                        x.parent = None
                    else:
                        if z.parent.right == z:
                            z.parent.right = x
                        if z.parent.left == z:
                            z.parent.left = x
                        x.parent = z.parent

                    x.right = y
                    y.parent = x

                    x.left = z
                    z.parent = x

                    # Updating the heights of the nodes
                    y.height = 1 + max(self.get_depth(y.left), self.get_depth(y.right))
                    z.height = 1 + max(self.get_depth(z.left), self.get_depth(z.right))
                    x.height = 1 + max(self.get_depth(x.left), self.get_depth(x.right))

                else:
                    x = y.right
                    T1 = y.left

                    # Restructuring
                    if self.get_root() == z:
                        self.root = y
                        y.parent = None
                    else:
                        if z.parent.right == z:
                            z.parent.right = y
                        if z.parent.left == z:
                            z.parent.left = y
                        y.parent = z.parent

                    y.left = z
                    z.parent = y

                    if T1:
                        z.right = T1
                        T1.parent = z
                    else:
                        z.right = None

                    # Updating the heights of the nodes
                    x.height = 1 + max(self.get_depth(x.left), self.get_depth(x.right))
                    z.height = 1 + max(self.get_depth(z.left), self.get_depth(z.right))
                    y.height = 1 + max(self.get_depth(y.left), self.get_depth(y.right))
            successor = successor.parent
        self.size -= 1
        return True


    ''''''''''''''''''
    '''Support Functions'''
    ''''''''''''''''''

    def _remove_helper(self, key):
        node_to_remove = self._find_helper(key, self.root)  # Searches for the node to remove
        successor = self.inorder_successor(node_to_remove)
        if node_to_remove:
            parent_to_ntr = node_to_remove.parent
            left_child_to_ntr = node_to_remove.left
            right_child_to_ntr = node_to_remove.right
            # If node to remove has no children.
            if left_child_to_ntr is None and right_child_to_ntr is None:
                # And it is the root.
                if node_to_remove == self.root:
                    self.root = None
                    return successor
                # Not the root and it is a left child of its parent.
                else:
                    if node_to_remove.key < parent_to_ntr.key:
                        parent_to_ntr.left = None
                        return successor
                    # Not the root and it is a right child of its parent.
                    else:
                        parent_to_ntr.right = None
                        return successor

            # If the node remove has only a left child
            elif left_child_to_ntr and right_child_to_ntr is None:
                # And it is the root.
                if node_to_remove == self.root:
                    self.root = left_child_to_ntr
                    left_child_to_ntr.parent = None
                    return successor
                else:
                    # Not the root and it is a left child of its parent.
                    if node_to_remove.key < parent_to_ntr.key:
                        parent_to_ntr.left = left_child_to_ntr
                        left_child_to_ntr.parent = parent_to_ntr
                        return successor
                    # Not the root and it is a right child of its parent.
                    else:
                        parent_to_ntr.right = left_child_to_ntr
                        left_child_to_ntr.parent = parent_to_ntr
                        return successor

            # If the node remove has only a right child
            elif right_child_to_ntr and left_child_to_ntr is None:
                # And it is the root.
                if node_to_remove == self.root:
                    self.root = right_child_to_ntr
                    right_child_to_ntr.parent = None
                    return successor
                else:
                    right_child_to_ntr.parent = parent_to_ntr
                    # Not the root and it is a left child of its parent.
                    if node_to_remove.key < parent_to_ntr.key:
                        parent_to_ntr.left = right_child_to_ntr
                        return successor
                    # Not the root and it is a right child of its parent.
                    else:
                        parent_to_ntr.right = right_child_to_ntr
                        return successor

            # If the node to remove has two children
            elif left_child_to_ntr and right_child_to_ntr:
                # If node to remove has no left granchild of the right child.
                if right_child_to_ntr.left is None:
                    # If the node to remove is the root
                    right_child_to_ntr.left = left_child_to_ntr
                    left_child_to_ntr.parent = right_child_to_ntr
                    if node_to_remove == self.root:
                        self.root = right_child_to_ntr
                        right_child_to_ntr.parent = None
                        return successor
                    # Otherwise
                    else:
                        right_child_to_ntr.parent = parent_to_ntr
                        if node_to_remove.key < parent_to_ntr.key:
                            parent_to_ntr.left = right_child_to_ntr
                            return successor
                        else:
                            parent_to_ntr.right = right_child_to_ntr
                            return successor
                # If node to remove has no right grandchild of the left child.
                elif left_child_to_ntr.right is None:
                    # If the node to remove is the root
                    left_child_to_ntr.right = right_child_to_ntr
                    right_child_to_ntr.parent = left_child_to_ntr
                    if node_to_remove == self.root:
                        self.root = left_child_to_ntr
                        left_child_to_ntr.parent = None
                        return successor
                    # Otherwise
                    else:
                        left_child_to_ntr.parent = parent_to_ntr
                        if node_to_remove.key < parent_to_ntr.key:
                            parent_to_ntr.left = left_child_to_ntr
                            return successor
                        else:
                            parent_to_ntr.right = left_child_to_ntr
                            return successor
                # All other options
                else:
                    temp_node = node_to_remove.right
                    while temp_node.left:
                        temp_node = temp_node.left
                    # If the node to be moved has a right child
                    if temp_node.right:
                        temp_node.right.parent = temp_node.parent
                        temp_node.parent.left = temp_node.right
                    temp_node.left = left_child_to_ntr
                    temp_node.right = right_child_to_ntr
                    left_child_to_ntr.parent = temp_node
                    right_child_to_ntr.parent = temp_node
                    # If node to remove is the root
                    if node_to_remove == self.root:
                        self.root = temp_node
                        temp_node.parent = None
                        return successor
                    # Otherwise
                    else:
                        temp_node.parent = parent_to_ntr
                        if node_to_remove.key < parent_to_ntr.key:
                            parent_to_ntr.left = temp_node
                            return successor
                        else:
                            parent_to_ntr.right = temp_node
                            return successor


    def _find_helper(self, key, cur):
        if cur is None:
            return None
        if cur.key == key:
            return cur
        elif key < cur.key:
            return self._find_helper(key, cur.left)
        else:
            return self._find_helper(key, cur.right)

    def to_array_helper(self, curr_node, array):
        if curr_node:
            array.append(curr_node.elem)
            if curr_node.left:
                self.to_array_helper(curr_node.left, array)
            if curr_node.right:
                self.to_array_helper(curr_node.right, array)
            return array

    def get_depth(self, cur):
        if cur is None:
            return -1
        return cur.height

    def get_balance(self, cur):
        if cur is None:
            return -1
        return self.get_depth(cur.left)-self.get_depth(cur.right)

    def _insert_helper(self, cur, new_node):

        if cur.key < new_node.key:
            if cur.right is None:
                cur.right = new_node
                new_node.parent = cur
            else:
                self._insert_helper(cur.right, new_node)
        else:
            if cur.left is None:
                cur.left = new_node
                new_node.parent = cur
            else:
                self._insert_helper(cur.left, new_node)

        cur.height = 1+max(self.get_depth(cur.left),self.get_depth(cur.right))

        #checking if the tree got unbalanced after the insertion
        if self.get_balance(cur) > 1:
            #Single rotation (right)
            if new_node.key < cur.left.key:
                z = cur
                y = cur.left
                x = y.left
                T2 = y.right

                #Restructuring
                if self.get_root()==z:
                    self.root = y
                    y.parent = None
                else:
                    if z.parent.left==z:
                        z.parent.left = y
                    if z.parent.right ==z:
                        z.parent.right =y
                    y.parent = z.parent

                y.right = z
                z.parent = y

                if T2:
                    z.left = T2
                    T2.parent = z
                else:
                    z.left = None

                #Updating the heights of the nodes
                x.height = 1 + max(self.get_depth(x.left), self.get_depth(x.right))
                z.height = 1 + max(self.get_depth(z.left), self.get_depth(z.right))
                y.height = 1 + max(self.get_depth(y.left), self.get_depth(y.right))

            #Double rotation (right)
            elif new_node.key > cur.left.key:
                z = cur
                y = cur.left
                x = y.right
                T1 = x.left
                T2 = x.right

                #Restructuring
                if self.get_root() == z:
                    self.root = x
                    x.parent = None
                else:
                    if z.parent.right == z:
                        z.parent.right = x
                    if z.parent.left == z:
                        z.parent.left = x
                    x.parent = z.parent

                x.left = y
                y.parent = x
                if T1:
                    y.right = T1
                    T1.parent = y
                else:
                    y.right = None
                x.right = z
                z.parent = x
                if T2:
                    z.left = T2
                    T2.parent = z
                else:
                    z.left = None

                #Updating the heights of the nodes
                y.height = 1 + max(self.get_depth(y.left), self.get_depth(y.right))
                z.height = 1 + max(self.get_depth(z.left), self.get_depth(z.right))
                x.height = 1 + max(self.get_depth(x.left), self.get_depth(x.right))

        elif self.get_balance(cur) < -1:
            # Double rotation (left)
            if new_node.key < cur.right.key:
                z = cur
                y = cur.right
                x = y.left
                if x:
                    T1 = x.left
                    T2 = x.right
                    if T1:
                        z.right = T1
                        T1.parent = z
                    else:
                        z.right = None
                    if T2:
                        y.left = T2
                        T2.parent = y
                    else:
                        y.left = None

                #Restructuring
                if self.get_root() == z:
                    self.root = x
                    x.parent = None
                else:
                    if z.parent.right == z:
                        z.parent.right = x
                    if z.parent.left == z:
                        z.parent.left = x
                    x.parent = z.parent

                x.right = y
                y.parent = x

                x.left = z
                z.parent = x

                # Updating the heights of the nodes
                y.height = 1 + max(self.get_depth(y.left), self.get_depth(y.right))
                z.height = 1 + max(self.get_depth(z.left), self.get_depth(z.right))
                x.height = 1 + max(self.get_depth(x.left), self.get_depth(x.right))

            #Single rotation(left)
            elif new_node.key > cur.right.key:
                z = cur
                y = cur.right
                x = y.right
                T1 = y.left

                #Restructuring
                if self.get_root() == z:
                    self.root = y
                    y.parent = None
                else:
                    if z.parent.right == z:
                        z.parent.right = y
                    if z.parent.left == z:
                        z.parent.left = y
                    y.parent = z.parent

                y.left = z
                z.parent = y

                if T1:
                    z.right = T1
                    T1.parent = z
                else:
                    z.right = None

                # Updating the heights of the nodes
                x.height = 1 + max(self.get_depth(x.left), self.get_depth(x.right))
                z.height = 1 + max(self.get_depth(z.left), self.get_depth(z.right))
                y.height = 1 + max(self.get_depth(y.left), self.get_depth(y.right))

    def inorder_successor(self,cur):
        #If the cur node has the right child
        if cur.right:
            node = cur.right
            #We search iteratively for the inorder successor in the right child of the cur node
            while node:
                if node.left is None:
                    break
                node = node.left
            return node
        #If the cur node has no right child, we go up to its parent
        parent = cur.parent
        while parent:
            #If the cur node is a left child of his parent, then the parent is the successor
            if cur != parent.right:
                break
            #If not, we analyse the parent of the parent in the same manner.
            cur = parent
            parent = parent.parent
        return parent


# Resources used to solve this exercise:
# https://www.geeksforgeeks.org/inorder-successor-in-binary-search-tree/
# https://www.geeksforgeeks.org/avl-tree-set-1-insertion/
# https://www.geeksforgeeks.org/avl-tree-set-2-deletion/

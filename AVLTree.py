#id1:
#name1:
#username1:
#id2:
#name2:
#username2:


"""A class represnting a node in an AVL tree"""

class AVLNode(object):
    """Constructor, you are allowed to add more fields. 
    
    @type key: int
    @param key: key of your node
    @type value: string
    @param value: data of your node
    """
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.height = -1


    """returns whether self is not a virtual node 

    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """
    def is_real_node(self):
        return self.left is not None and self.right is not None and self.height != -1


"""
A class implementing an AVL tree.
"""

class AVLTree(object):

    """
    Constructor, you are allowed to add more fields.
    """
    def __init__(self):
        self.root = None
        self._max_node = None
        self._size = 0

    def update_node_height(self, node):

        def rec(node):
            if node.is_real_node() == False:
                return 0
            else:
                return max(rec(node.left), rec(node.right)) + 1

        node.height = max(rec(node.left), rec(node.right))

        return


    """searches for a node in the dictionary corresponding to the key (starting at the root)
        
    @type key: int
    @param key: a key to be searched
    @rtype: (AVLNode,int)
    @returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
    and e is the number of edges on the path between the starting node and ending node+1.
    """
    def search(self, key):

        node = self.root
        arcs = 1

        while True:
            if node.key == key:
                return node, arcs

            elif node.key > key:
                if node.left.is_real_node() == False is None:
                    return None, -1
                else:
                    node = node.left

            elif node.key < key:
                if node.right.is_real_node() == False:
                    return None, -1
                else:
                    node = node.right

            arcs += 1


    """searches for a node in the dictionary corresponding to the key, starting at the max
        
    @type key: int
    @param key: a key to be searched
    @rtype: (AVLNode,int)
    @returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
    and e is the number of edges on the path between the starting node and ending node+1.
    """
    def finger_search(self, key):
        return None, -1

    def insert(self, key, val):
        """inserts a new node into the dictionary with corresponding key and value, starting at the max

        @type key: int
        @pre: key currently does not appear in the dictionary
        @param key: key of item that is to be inserted to self
        @type val: string
        @param val: the value of the item
        @rtype: (AVLNode,int,int)
        @returns: a 3-tuple (x,e,h) where x is the new node,
        e is the number of edges on the path between the starting node and new node before rebalancing,
        and h is the number of PROMOTE cases during the AVL rebalancing
        """
        node, val = self.search(key)
        if val != -1:
            return None, -1, -1

        node = self.root
        while True:
            if key > node.key:
                node = node.left
            else:
                node = node.right

            if not node.is_real_node():
                node.key = key
                node.val = val
                node.height = 0
                node.left, node.right = AVLNode(), AVLNode()
                break

        ############## update tree max, size #################

        criminal_node = node
        child_node = None
        grandchild_node = None

        while self.root != criminal_node:

            grandchild = child_node
            child_node = criminal_node
            criminal_node = criminal_node.parent

            self.update_node_height(child_node.right)
            self.update_node_height(child_node.left)

            criminal_node_bf = child_node.left.height - child_node.right.height

            if abs(criminal_node_bf) == 2:

                child_node_bf = child_node.left.height - child_node.right.height

                if criminal_node_bf == 2 and child_node_bf == 1:  ## right rotation. a.k.a

                    if criminal_node is self.root:
                        self.root = child_node
                    else:  # swap_correct_son(criminal.parent, child) function
                        if criminal_node.parent.left.key == criminal_node.key:
                            criminal_node.parent.left = child_node
                        else:
                            criminal_node.parent.right = child_node

                    child_node.parent = criminal_node.parent
                    criminal_node.parent = child_node
                    child_node.right = criminal_node
                    criminal_node.left = child_node.right
                    criminal_node.left.parent = criminal_node

                elif criminal_node_bf == 2 and child_node_bf == 1:  ## left then right rotation
                    pass

                elif criminal_node_bf == -2 and child_node_bf == -1:  ## left rotation

                    if criminal_node is self.root:
                        self.root = child_node
                    else:  # swap_correct_son(criminal.parent, child) function
                        if criminal_node.parent.left.key == criminal_node.key:
                            criminal_node.parent.left = child_node
                        else:
                            criminal_node.parent.right = child_node

                    child_node.parent = criminal_node.parent
                    criminal_node.parent = child_node
                    child_node.left = criminal_node
                    criminal_node.right = child_node.left
                    criminal_node.right.parent = criminal_node

                elif criminal_node_bf == -2 and child_node_bf == 1:
                    pass

        return None, -1, -1



    """inserts a new node into the dictionary with corresponding key and value (starting at the root)

    @type key: int
    @pre: key currently does not appear in the dictionary
    @param key: key of item that is to be inserted to self
    @type val: string
    @param val: the value of the item
    @rtype: (AVLNode,int,int)
    @returns: a 3-tuple (x,e,h) where x is the new node,
    e is the number of edges on the path between the starting node and new node before rebalancing,
    and h is the number of PROMOTE cases during the AVL rebalancing
    """
    def insert(self, key, val):
        node = None
        edges = -1
        promotes = -1

        if self.root is None:
            node = AVLNode(key, val)
            self.root = node
            self.root.height = 0
            self.root.right = AVLNode()
            self.root.left = AVLNode()
            self._max_node = self.root
        else:
            # find location to insert + insert
            if key < self.root.key:
                node = AVLNode(key, val)
                node.right = AVLNode()
                node.left = AVLNode()
                self.root.left = node
                node.parent = self.root
                node.height = 0
                # go up the tree parents and fix heights
                self.root.height = 1
            else:
                node = AVLNode(key, val)
                node.right = AVLNode()
                node.left = AVLNode()
                self.root.right = node
                node.parent = self.root
                node.height = 0
                # go up the tree parents and fix heights
                self.root.height = 1

        if self._max_node.key < key:
            self._max_node = node

        self._size += 1

        return node, edges, promotes

        # "search" if exists, if returns -1 doesn't exist
        # insert in the correct location (create node, set virtual false, height=0, left and right vnode false, key, value
        # update tree max, size
        # store criminal_node=inserted_node, child=None, grandchild=None
        # start going up (while loop) criminal is not self.root
        #   grandchild = child
        #   child = criminal
        #   criminal = criminal.parent
        #   criminal_bf = child.left.height - child.right.height
        #   # maybe don't continue going up later
        #   if abs(crimial_bf) == 2:
        #       child_bf = child.left.height - child.right.height
        #       # get correct use case, address root as a sub case
        #       # criminal: +2, child +1 ==> right rotation. a.k.a
        #           criminal_parent = criminal.parent
        #           criminal.parent = child
        #           if criminal is self.root:
        #               self.root = child
        #               child.parent = None
        #           else:
        #               swap_correct_son(criminal.parent, child)
        #           criminal.left = child.right
        #           child.right.parent = criminal
        #           child.right = criminal
        #       # criminal: -2, child -1 ==> left rotation.
        #           criminal_parent = criminal.parent
        #           criminal.parent = child
        #           if criminal is self.root:
        #               self.root = child
        #               child.parent = None
        #           else:
        #               swap_correct_son(criminal.parent, child)
        #           criminal.right = child.left
        #           child.left.parent = criminal
        #           child.left = criminal


    """inserts a new node into the dictionary with corresponding key and value, starting at the max
    """
    def finger_insert(self, key, val):
        return None, -1, -1


    """deletes node from the dictionary
    """
    def delete(self, node):
        return    


    """joins self with item and another AVLTree
    """
    def join(self, tree2, key, val):
        return


    """splits the dictionary at a given node
    """
    def split(self, node):
        return None, None


    """returns an array representing dictionary 
    """
    def avl_to_array(self):
        array = list()
        self._create_in_order_list(self.root, array)
        return array

    def _create_in_order_list(self, x, lst=None):
        if not x.is_real_node():
            return
        self._create_in_order_list(x.left, lst)
        lst.append((x.key, x.value))
        self._create_in_order_list(x.right, lst)


    # ==================== HELPER FUNCTIONS I ADDED ====================

    def print_tree(self, node=None, indent="", last=True):
        if node is None:
            node = self.root

        if node is None or not node.is_real_node():
            print("(empty tree)")
            return

        if node.right is not None and node.right.is_real_node():
            new_indent = indent + ("│   " if last else "    ")
            self.print_tree(node.right, new_indent, False)

        left_h = node.left.height
        right_h = node.right.height
        bf = left_h - right_h

        connector = "└── " if last else "┌── "
        print(f"{indent}{connector}{node.key} [h={node.height}, bf={bf}]")

        if node.left is not None and node.left.is_real_node():
            new_indent = indent + ("    " if last else "│   ")
            self.print_tree(node.left, new_indent, True)


    def validate_heights(self):
        ok, _ = self._validate_heights_rec(self.root)
        return ok

    def _validate_heights_rec(self, node):
        if not node.is_real_node():
            return True, -1

        left_ok, left_h = self._validate_heights_rec(node.left)
        right_ok, right_h = self._validate_heights_rec(node.right)

        expected = 1 + max(left_h, right_h)

        if not node.height == expected:
            print(f"[HEIGHT ERROR] key={node.key}, stored={node.height}, expected={expected}")

        return (left_ok and right_ok and node.height == expected), expected


    def validate_balance_factors(self):
        return self._validate_bf_rec(self.root)

    def _validate_bf_rec(self, node):
        if node is None or not node.is_real_node():
            return True

        bf = node.left.height - node.right.height

        ok_here = -1 <= bf <= 1
        if not ok_here:
            print(f"[BF ERROR] key={node.key}, bf={bf}, left_h={left_h}, right_h={right_h}")

        left_ok = self._validate_bf_rec(node.left)
        right_ok = self._validate_bf_rec(node.right)

        return ok_here and left_ok and right_ok


    # ==================== HELPER FUNCTIONS I ADDED ====================


    def max_node(self):
        return self._max_node

    def size(self):
        return self._size  


    def get_root(self):
        return self.root



#### TO DELETE ####

if __name__ == "__main__":
    T = AVLTree()
    T.insert(10, "10")
    T.insert(5, "5")
    T.insert(15, "15")
    print(T.size())
    print(T.avl_to_array())
    print(T.get_root().value)
    print(T.max_node().value)
    print(T.validate_heights())
    print(T.validate_balance_factors())
    T.print_tree()

# id1:
# name1:
# username1:
# id2:
# name2:
# username2:


"""A class represnting a node in an AVL tree"""
from sympy import false
from sympy.codegen.ast import continue_


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


    def search(self, key):
        """searches for a node in the dictionary corresponding to the key (starting at the root)

        @type key: int
        @param key: a key to be searched
        @rtype: (AVLNode,int)
        @returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
        and e is the number of edges on the path between the starting node and ending node+1.
        """
        node = self.root
        arcs = 1

        if node is None:
            return None, -1

        if node.is_real_node() == False:
            return None, -1

        while node.is_real_node():
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

        return None, -1


    def finger_search(self, key):
        """searches for a node in the dictionary corresponding to the key, starting at the max

        @type key: int
        @param key: a key to be searched
        @rtype: (AVLNode,int)
        @returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
        and e is the number of edges on the path between the starting node and ending node+1.
        """
        node = self._max_node
        arcs = 1

        #======== Traverse Up ======================
        continue_ = True
        print(node.key)
        while node != self.root:
            if node.key == key:
                return node, arcs
            if key <= node.parent.key:
                node = node.parent
            else:
                break
            arcs += 1

        #======== Traverse down ======================
        while node.is_real_node():
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

        #-------------- simple insertion --------------------
        x, e = self.simple_insert(key, val)
        self.set_heights_from_node_up(x)
        h = 0
        #---------------------------------------------------

        #------------- update tree max, size ------------------
        self._size += 1
        if self._max_node is None or self._max_node.key < x.key:
            self._max_node = x
        #-----------------------------------------------------

        #------------- Balance Tree ----------------------------
        criminal_node = x
        child_node = None
        grandchild_node = None
        continue_loop = True

        while criminal_node != self.root and continue_loop:

            grandchild_node = child_node
            child_node = criminal_node
            criminal_node = criminal_node.parent

            criminal_node_bf = criminal_node.left.height - criminal_node.right.height
            child_node_bf = child_node.left.height - child_node.right.height

            if abs(criminal_node_bf) == 2: # found the place to do the balance
                continue_loop = False

                if criminal_node_bf == -2 and child_node_bf == -1: #left rotation
                    self.left_rotation(criminal_node, child_node)
                    h = 1
                elif criminal_node_bf == -2 and child_node_bf == 1: #right then left rotation
                    self.right_then_left_rotation(criminal_node, child_node, grandchild_node)
                    h = 2
                elif criminal_node_bf == 2 and child_node_bf == -1: #right then left rotation
                    self.left_then_right_rotation(criminal_node, child_node, grandchild_node)
                    h = 2
                elif criminal_node_bf == 2 and child_node_bf == 1: #right rotation
                    self.right_rotation(criminal_node, child_node)
                    h = 1
        #---------------------------------------------------------------

        return x, e, h


    def finger_insert(self, key, val):
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


        #-------------- simple insertion --------------------
        x, e = self.finger_simple_insert(key, val)
        self.set_heights_from_node_up(x)
        h = 0
        #---------------------------------------------------

        #------------- update tree max, size ------------------
        self._size += 1
        if self._max_node is None or self._max_node.key < x.key:
            self._max_node = x
        #-----------------------------------------------------

        #------------- Balance Tree ----------------------------
        criminal_node = x
        child_node = None
        grandchild_node = None
        continue_loop = True

        while criminal_node != self.root and continue_loop:

            grandchild_node = child_node
            child_node = criminal_node
            criminal_node = criminal_node.parent

            criminal_node_bf = criminal_node.left.height - criminal_node.right.height
            child_node_bf = child_node.left.height - child_node.right.height

            if abs(criminal_node_bf) == 2: # found the place to do the balance
                continue_loop = False

                if criminal_node_bf == -2 and child_node_bf == -1: #left rotation
                    self.left_rotation(criminal_node, child_node)
                    h = 1
                elif criminal_node_bf == -2 and child_node_bf == 1: #right then left rotation
                    self.right_then_left_rotation(criminal_node, child_node, grandchild_node)
                    h = 2
                elif criminal_node_bf == 2 and child_node_bf == -1: #right then left rotation
                    self.left_then_right_rotation(criminal_node, child_node, grandchild_node)
                    h = 2
                elif criminal_node_bf == 2 and child_node_bf == 1: #right rotation
                    self.right_rotation(criminal_node, child_node)
                    h = 1
        #---------------------------------------------------------------

        return x, e, h


    def delete(self, node):
        """deletes node from the dictionary

        @type node: AVLNode
        @pre: node is a real pointer to a node in self
        """
        return


    def join(self, tree2, key, val):
        """joins self with item and another AVLTree

        @type tree2: AVLTree
        @param tree2: a dictionary to be joined with self
        @type key: int
        @param key: the key separting self and tree2
        @type val: string
        @param val: the value corresponding to key
        @pre: all keys in self are smaller than key and all keys in tree2 are larger than key,
        or the opposite way
        """
        return


    def split(self, node):
        """splits the dictionary at a given node

        @type node: AVLNode
        @pre: node is in self
        @param node: the node in the dictionary to be used for the split
        @rtype: (AVLTree, AVLTree)
        @returns: a tuple (left, right), where left is an AVLTree representing the keys in the
        dictionary smaller than node.key, and right is an AVLTree representing the keys in the
        dictionary larger than node.key.
        """
        return None, None


    def avl_to_array(self):
        """returns an array representing dictionary
        @rtype: list
        @returns: a sorted list according to key of touples (key, value) representing the data structure
        """
        array = list()
        self._create_in_order_list(self.root, array)

        return array


    def max_node(self):
        """returns the number of items in dictionary
        @rtype: int
        @returns: the number of items in dictionary
        """
        return self._max_node


    def size(self):
        """returns the root of the tree representing the dictionary
        @rtype: AVLNode
        @returns: the root, None if the dictionary is empty
        """
        return self._size


    def get_root(self):
        return self.root


    # ==================== HELPER FUNCTIONS =============================

    def set_heights_from_node_up(self, node, arg='Insertion'):

        counter = node.height
        while node.parent is not None:
            counter += 1
            if node.parent.height < counter or arg == 'Rotation':
                node.parent.height = counter
            node = node.parent

        return


    def simple_insert(self, key, val):

        arcs = 0

        if self.root is None:
            new_node = AVLNode(key, val)
            self.root = new_node
            self.root.height = 0
            self.root.right = AVLNode()
            self.root.left = AVLNode()
            self._max_node = self.root
        else:
            node = self.root
            while node.is_real_node():
                arcs += 1
                if key > node.key:
                    if node.right.is_real_node():
                        node = node.right
                    else:
                        new_node = AVLNode(key, val)
                        new_node.parent = node
                        new_node.height = 0
                        new_node.left = AVLNode()
                        new_node.right = AVLNode()
                        node.right = new_node
                        break
                else:
                    if node.left.is_real_node():
                        node = node.left
                    else:
                        new_node = AVLNode(key, val)
                        new_node.parent = node
                        new_node.height = 0
                        new_node.left = AVLNode()
                        new_node.right = AVLNode()
                        node.left = new_node
                        break

        return new_node, arcs


    def finger_simple_insert(self, key, val):

        arcs = 0

        if self.root is None:
            new_node = AVLNode(key, val)
            self.root = new_node
            self.root.height = 0
            self.root.right = AVLNode()
            self.root.left = AVLNode()
            self._max_node = self.root
        else:
            # ======== Traverse Up ======================
            continue_ = True
            node = self._max_node
            while node != self.root and continue_:
                if key < node.parent.key:
                    node = node.parent
                else:
                    continue_ = False
                arcs += 1

            # ======== Traverse Down ======================
            while node.is_real_node():
                arcs += 1
                if key > node.key:
                    if node.right.is_real_node():
                        node = node.right
                    else:
                        new_node = AVLNode(key, val)
                        new_node.parent = node
                        new_node.height = 0
                        new_node.left = AVLNode()
                        new_node.right = AVLNode()
                        node.right = new_node
                        break
                else:
                    if node.left.is_real_node():
                        node = node.left
                    else:
                        new_node = AVLNode(key, val)
                        new_node.parent = node
                        new_node.height = 0
                        new_node.left = AVLNode()
                        new_node.right = AVLNode()
                        node.left = new_node
                        break

        return new_node, arcs

    #====================================================================

    #========== Validating and testing functions ========================

    def _create_in_order_list(self, x, lst=None):
        if not x.is_real_node():
            return
        self._create_in_order_list(x.left, lst)
        lst.append((x.key, x.value))
        self._create_in_order_list(x.right, lst)


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

        left_h = node.left.height
        right_h = node.right.height
        bf = left_h - right_h

        ok_here = -1 <= bf <= 1
        if not ok_here:
            print(f"[BF ERROR] key={node.key}, bf={bf}, left_h={left_h}, right_h={right_h}")

        left_ok = self._validate_bf_rec(node.left)
        right_ok = self._validate_bf_rec(node.right)

        return ok_here and left_ok and right_ok

    # =====================================================================

    # ==================== HELPER ROTATION FUNCTIONS ==================================

    def left_rotation(self, criminal_node, child_node):

        if criminal_node is self.root:
            self.root = child_node
            criminal_node.parent = child_node
            child_node.parent = None
        else:  # swap_correct_son(criminal.parent, child) function
            if criminal_node.parent.left == criminal_node:
                criminal_node.parent.left = child_node
            else:
                criminal_node.parent.right = child_node
            child_node.parent = criminal_node.parent
            criminal_node.parent = child_node

        criminal_node.right = child_node.left
        child_node.left = criminal_node

        criminal_node.left.parent = criminal_node

        criminal_node.height = criminal_node.height - 2
        self.set_heights_from_node_up(criminal_node, 'Rotation')

        return

    def right_then_left_rotation(self, criminal_node, child_node, grandchild_node):

        if criminal_node is self.root:
            self.root = grandchild_node
        else:  # swap_correct_son(criminal.parent, child) function
            if criminal_node.parent.left == criminal_node:
                criminal_node.parent.left = grandchild_node
            else:
                criminal_node.parent.right = grandchild_node

        grandchild_node.parent = criminal_node.parent

        criminal_node.right = grandchild_node.right
        child_node.left = grandchild_node.left
        criminal_node.right.parent = criminal_node
        child_node.left.parent = child_node

        grandchild_node.right = child_node
        grandchild_node.left = criminal_node

        criminal_node.parent = grandchild_node
        child_node.parent = grandchild_node

        criminal_node.height = criminal_node.height - 2
        self.set_heights_from_node_up(criminal_node, 'Rotation')
        child_node.height = child_node.height - 1
        self.set_heights_from_node_up(child_node, 'Rotation')

        return

    def left_then_right_rotation(self, criminal_node, child_node, grandchild_node):

        if criminal_node is self.root:
            self.root = grandchild_node
        else:  # swap_correct_son(criminal.parent, child) function
            if criminal_node.parent.left == criminal_node:
                criminal_node.parent.left = grandchild_node
            else:
                criminal_node.parent.right = grandchild_node

        grandchild_node.parent = criminal_node.parent

        criminal_node.left = grandchild_node.right
        child_node.right = grandchild_node.left
        criminal_node.left.parent = criminal_node
        child_node.right.parent = child_node

        grandchild_node.left = child_node
        grandchild_node.right = criminal_node

        criminal_node.parent = grandchild_node
        child_node.parent = grandchild_node

        criminal_node.height = criminal_node.height - 2
        self.set_heights_from_node_up(criminal_node, 'Rotation')
        child_node.height = child_node.height - 1
        self.set_heights_from_node_up(child_node, 'Rotation')

        return

    def right_rotation(self, criminal_node, child_node):

        if criminal_node is self.root:
            self.root = child_node
            criminal_node.parent = child_node
            child_node.parent = None
        else:  # swap_correct_son(criminal.parent, child) function
            if criminal_node.parent.left == criminal_node:
                criminal_node.parent.left = child_node
            else:
                criminal_node.parent.right = child_node
            child_node.parent = criminal_node.parent
            criminal_node.parent = child_node

        criminal_node.left = child_node.right
        child_node.right = criminal_node

        criminal_node.left.parent = criminal_node

        criminal_node.height = criminal_node.height - 2
        self.set_heights_from_node_up(criminal_node, 'Rotation')

        return

    # ====================================================================

if __name__ == "__main__":

    ##regular insertions test
    T = AVLTree()
    T.insert(15, "15")
    T.insert(10, "10")
    T.insert(22, "22")
    T.insert(4, "4")
    T.insert(11, "11")
    T.insert(20, "20")
    T.insert(24, "24")
    T.insert(2, "2")
    T.insert(7, "7")
    T.insert(12, "12")
    T.insert(18, "18")
    T.insert(1, "1")
    T.insert(6, "6")
    T.insert(8, "8")
    T.insert(5, "5")
    T.print_tree()

    ##finger insertions test
    T2 = AVLTree()
    T2.finger_insert(15, "15")
    T2.finger_insert(10, "10")
    T2.finger_insert(22, "22")
    T2.finger_insert(4, "4")
    T2.finger_insert(11, "11")
    T2.finger_insert(20, "20")
    T2.finger_insert(24, "24")
    T2.finger_insert(2, "2")
    T2.finger_insert(7, "7")
    T2.finger_insert(12, "12")
    T2.finger_insert(18, "18")
    T2.finger_insert(1, "1")
    T2.finger_insert(6, "6")
    T2.finger_insert(8, "8")
    T2.finger_insert(5, "5")
    T2.print_tree()

    ##other tests
    print(T.size())
    print(T.avl_to_array())
    print(T.get_root().value)
    print(T.max_node().value)
    print(T.validate_heights())
    print(T.validate_balance_factors())
    T.print_tree()

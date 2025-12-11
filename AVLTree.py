# id1:
# name1:
# username1:
# id2:
# name2:
# username2:


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
        self.virtual_node = AVLNode()


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

        #simple insertion
        x, e = self.simple_insert(self.root, key, val)
        self.set_heights_from_node_up(x)
        h = 0

        #update tree max, size
        self._size += 1
        if self._max_node is None or self._max_node.key < x.key:
            self._max_node = x

        #Balance Tree
        h = self.tree_balancer(x, "One Balance")

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

        # Traverse Up
        arcs = 0
        node = self.root
        if self.root is not None:
            continue_ = True
            node = self._max_node
            while node != self.root and continue_:
                if key < node.parent.key:
                    node = node.parent
                else:
                    continue_ = False
                arcs += 1

        # Simple insert from the common node
        x, e = self.simple_insert(node, key, val)
        e += arcs
        self.set_heights_from_node_up(x)

        #update tree max, size
        self._size += 1
        if self._max_node is None or self._max_node.key < x.key:
            self._max_node = x

        #Balance Tree
        h = 0
        h = self.tree_balancer(x, "One Balance")


        return x, e, h


    def delete(self, node):
        """deletes node from the dictionary

        @type node: AVLNode
        @pre: node is a real pointer to a node in self
        """
        #Simle Delete of the node

        y, original_y_parent = self.simple_delete(node)

        #balance Tree
        if original_y_parent is not node:
            start_node = original_y_parent
        else:
            start_node = y

        self.tree_balancer(start_node)

        #update tree max, size
        self._size -= 1
        if self._max_node == node:
            iter_node = self.root
            while iter_node.right.is_real_node():
                iter_node = iter_node.right
            self._max_node = iter_node

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
        # handle trivial empty cases
        if self.root is None and tree2.root is None:
            new_root = AVLNode(key, val)
            new_root.left = self.virtual_node
            new_root.right = self.virtual_node
            new_root.height = 0
            self.root = new_root
            self._size = 1
            self._max_node = new_root
            return

        if self.root is None:
            # build result on top of tree2 and copy it into self
            x, _, _ = tree2.insert(key, val)
            self.root = tree2.root
            self._size = tree2._size
            # recompute max node
            max_node = self.root
            while max_node.right.is_real_node():
                max_node = max_node.right
            self._max_node = max_node
            return

        if tree2.root is None:
            # symmetric: just insert into self
            self.insert(key, val)
            return

        # decide who is the "left" tree and who is the "right" tree
        # left_tree_root: all keys smaller than key
        # right_tree_root: all keys larger than key
        if self.root.key < key:
            left_tree_root = self.root
            left_tree = self
            right_tree_root = tree2.root
            right_tree = tree2
        else:
            left_tree_root = tree2.root
            left_tree = tree2
            right_tree_root = self.root
            right_tree = self

        h_left = left_tree_root.height
        h_right = right_tree_root.height

        # create the separating node
        new_node = AVLNode(key, val)
        new_node.left = self.virtual_node
        new_node.right = self.virtual_node
        new_node.height = 0

        root_after = None

        # case 1: heights differ by at most 1
        if abs(h_left - h_right) <= 1:
            new_node.left = left_tree_root
            new_node.right = right_tree_root
            left_tree_root.parent = new_node
            right_tree_root.parent = new_node
            new_node.height = 1 + max(h_left, h_right)

            root_after = new_node
        
        # case 2: left tree is higher
        elif h_left > h_right:
            current = left_tree_root
            # walk down the right spine until right child has height <= h_right
            while current.right.height > h_right:
                current = current.right

            new_node.left = current.right
            new_node.right = right_tree_root

            if current.right.is_real_node():
                current.right.parent = new_node
            if right_tree_root.is_real_node():
                right_tree_root.parent = new_node

            current.right = new_node
            new_node.parent = current

            # Update heights and balance
            new_node.height = 1 + max(new_node.left.height, new_node.right.height)
            left_tree.set_heights_from_node_up(new_node)
            left_tree.tree_balancer(new_node)
    
            # Find root by traversing up from new_node
            root_after = new_node
            while root_after.parent is not None:
                root_after = root_after.parent

        # case 3: right tree is higher
        else:  # h_right > h_left
            current = right_tree_root
            # walk down the left spine until left child has height <= h_left
            while current.left.height > h_left:
                current = current.left

            new_node.right = current.left
            new_node.left = left_tree_root

            if current.left.is_real_node():
                current.left.parent = new_node
            if left_tree_root.is_real_node():
                left_tree_root.parent = new_node

            current.left = new_node
            new_node.parent = current

            # Update heights and balance
            new_node.height = 1 + max(new_node.left.height, new_node.right.height)
            right_tree.set_heights_from_node_up(new_node)
            right_tree.tree_balancer(new_node)

            # Find root by traversing up from new_node
            root_after = new_node
            while root_after.parent is not None:
                root_after = root_after.parent
        
        self.root = root_after
        
        # update size and recompute max_node
        self._size = self._size + tree2._size + 1
        max_node = self.root
        while max_node.right.is_real_node():
            max_node = max_node.right
        self._max_node = max_node


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

    def tree_balancer(self, start_node, arg='Default'):

        h = 0

        criminal_node = start_node
        continue_ = True

        while criminal_node is not None and criminal_node.is_real_node() and continue_:

            criminal_node_bf = criminal_node.left.height - criminal_node.right.height

            if abs(criminal_node_bf) == 2:  # found the place to do the balance

                if arg == 'One Balance':
                    continue_ = False

                if criminal_node_bf == -2:  # check the right son

                    child_node = criminal_node.right
                    child_node_bf = child_node.left.height - child_node.right.height

                    if child_node_bf == -1 or not child_node.right.is_real_node():  # left rotation
                        self.left_rotation(criminal_node, child_node)
                        h = 1

                    elif child_node_bf in [0, 1]:  # right then left rotation
                        grandchild_node = child_node.left
                        self.right_then_left_rotation(criminal_node, child_node, grandchild_node)
                        h = 2

                elif criminal_node_bf == 2:  # check the left son

                    child_node = criminal_node.left
                    child_node_bf = child_node.left.height - child_node.right.height

                    if child_node_bf in [0, -1]:  # right then left rotation

                        grandchild_node = child_node.right
                        self.left_then_right_rotation(criminal_node, child_node, grandchild_node)
                        h = 2

                    elif child_node_bf == 1:  # right rotation

                        self.right_rotation(criminal_node, child_node)
                        h = 1

            criminal_node = criminal_node.parent

        return h


    def set_heights_from_node_up(self, node):

        while node is not None and node.is_real_node():
            node.height = max(node.left.height, node.right.height) + 1
            node = node.parent

        return
    

    def simple_insert(self, start_node, key, val):

        arcs = 0

        if self.root is None:
            new_node = AVLNode(key, val)
            self.root = new_node
            self.root.height = 0
            self.root.right = self.virtual_node
            self.root.left = self.virtual_node
            self._max_node = self.root
        else:
            node = start_node
            while node.is_real_node():
                arcs += 1
                if key > node.key:
                    if node.right.is_real_node():
                        node = node.right
                    else:
                        new_node = AVLNode(key, val)
                        new_node.parent = node
                        new_node.height = 0
                        new_node.left = self.virtual_node
                        new_node.right = self.virtual_node
                        node.right = new_node
                        break
                else:
                    if node.left.is_real_node():
                        node = node.left
                    else:
                        new_node = AVLNode(key, val)
                        new_node.parent = node
                        new_node.height = 0
                        new_node.left = self.virtual_node
                        new_node.right = self.virtual_node
                        node.left = new_node
                        break

        return new_node, arcs


    def simple_delete(self, node):

        if node is None or not node.is_real_node():
            return self.virtual_node, None

        ##first case - node is leaf

        if node is not self.root and node.parent is not None:
            y_node, original_y_parent = node.parent, node.parent.left

        if not node.left.is_real_node() and not node.right.is_real_node():

            if node.parent.left == node:
                node.parent.left = self.virtual_node
            elif node.parent.right == node:
                node.parent.right = self.virtual_node

            self.set_heights_from_node_up(node.parent)

        ##second case - node has one child
        elif node.right.is_real_node() and not node.left.is_real_node(): # has right child

            if node.parent.left == node:
                node.parent.left = node.right
            elif node.parent.right == node:
                node.parent.right = node.right

            self.set_heights_from_node_up(node.parent)

        elif node.left.is_real_node() and not node.right.is_real_node():  # has left child

            if node.parent.left == node:
                node.parent.left = node.left
            elif node.parent.right == node:
                node.parent.right = node.left

            self.set_heights_from_node_up(node.parent)

        ##third case - node has two children
        elif node.right.is_real_node() and node.left.is_real_node():

            iter_node = node.right

            while iter_node.left.is_real_node():
                iter_node = iter_node.left
            y_node, original_y_parent = iter_node, iter_node.parent
            iter_node.right.parent = iter_node.parent
            iter_node.parent.left = iter_node.right

            if node.parent.left == node:
                node.parent.left = iter_node
            elif node.parent.right == node:
                node.parent.right = iter_node

            height_check_node = iter_node.parent.right
            iter_node.parent = node.parent
            iter_node.left = node.left
            iter_node.right = node.right
            node.left.parent = iter_node
            node.right.parent = iter_node

            self.set_heights_from_node_up(height_check_node)

        return y_node, original_y_parent


    #====================================================================

    #========== Validating and testing functions ========================

    def _create_in_order_list(self, x, lst=None):
        if not x.is_real_node():
            return
        self._create_in_order_list(x.left, lst)
        lst.append((x.key, x.value))
        self._create_in_order_list(x.right, lst)


    def print_tree(self, node =None, indent="", last=True):
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
        
        if criminal_node.right.is_real_node():
            criminal_node.right.parent = criminal_node

        criminal_node.height = criminal_node.height - 2
        self.set_heights_from_node_up(criminal_node)

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

        criminal_node.right = grandchild_node.left
        child_node.left = grandchild_node.right
        
        if criminal_node.right.is_real_node():
            criminal_node.right.parent = criminal_node
        if child_node.left.is_real_node():
            child_node.left.parent = child_node

        grandchild_node.right = child_node
        grandchild_node.left = criminal_node

        criminal_node.parent = grandchild_node
        child_node.parent = grandchild_node

        criminal_node.height = criminal_node.height - 2
        self.set_heights_from_node_up(criminal_node)
        child_node.height = child_node.height - 1
        self.set_heights_from_node_up(child_node)

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
        if criminal_node.left.is_real_node():
            criminal_node.left.parent = criminal_node
        if child_node.right.is_real_node():
            child_node.right.parent = child_node

        grandchild_node.left = child_node
        grandchild_node.right = criminal_node

        criminal_node.parent = grandchild_node
        child_node.parent = grandchild_node

        criminal_node.height = criminal_node.height - 2
        self.set_heights_from_node_up(criminal_node)
        child_node.height = child_node.height - 1
        self.set_heights_from_node_up(child_node)

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

        if criminal_node.left.is_real_node():
            criminal_node.left.parent = criminal_node

        criminal_node.height = criminal_node.height - 2
        self.set_heights_from_node_up(criminal_node)

        return

    # ====================================================================




def build_avl_from_list(lst):
    """
    Helper: build an AVLTree from a list of (key, value) pairs.
    Insert in given order (not sorted) to create different shapes.
    """
    t = AVLTree()
    for k, v in lst:
        t.insert(k, v)
    return t


def check_avl(tree, label=""):
    """
    Helper: print tree + basic validation.
    """
    print(f"\n=== {label} ===")
    tree.print_tree()
    in_order = tree.avl_to_array()
    print("In-order keys:", [k for (k, _) in in_order])
    ok_h = tree.validate_heights()
    ok_bf = tree.validate_balance_factors()
    print("valid heights:", ok_h)
    print("valid BF     :", ok_bf)
    return ok_h and ok_bf


def test_join_case_empty_trees():
    print("\n================= test_join_case_empty_trees =================")
    T1 = AVLTree()
    T2 = AVLTree()
    # join(T2) into T1 with middle key 10
    T1.join(T2, 10, "10")
    assert check_avl(T1, "empty + empty")
    assert T1.avl_to_array() == [(10, "10")]


def test_join_self_empty():
    print("\n================= test_join_self_empty =================")
    # self empty, tree2 non-empty
    T1 = AVLTree()
    T2 = build_avl_from_list([(1, "1"), (3, "3"), (5, "5"), (7, "7")])
    # all keys in T2 < 10
    T1.join(T2, 10, "10")
    assert check_avl(T1, "self empty, tree2 non-empty")
    keys = [k for (k, _) in T1.avl_to_array()]
    assert keys == [1, 3, 5, 7, 10]


def test_join_tree2_empty():
    print("\n================= test_join_tree2_empty =================")
    # self non-empty, tree2 empty
    T1 = build_avl_from_list([(1, "1"), (3, "3"), (5, "5")])
    T2 = AVLTree()
    # we just insert key normally according to your join implementation
    before = [k for (k, _) in T1.avl_to_array()]
    T1.join(T2, 10, "10")
    assert check_avl(T1, "self non-empty, tree2 empty")
    keys = [k for (k, _) in T1.avl_to_array()]
    assert keys == before + [10]


def test_join_same_height():
    print("\n================= test_join_same_height =================")
    # Build two trees with roughly same height
    T1 = build_avl_from_list([(1, "1"), (2, "2"), (3, "3"), (0, "0")])
    T2 = build_avl_from_list([(10, "10"), (11, "11"), (12, "12"), (13, "13")])
    # ensure all keys in T1 < 5 < all keys in T2
    T1.join(T2, 5, "5")
    assert check_avl(T1, "join: same height")
    keys = [k for (k, _) in T1.avl_to_array()]
    assert keys == [0, 1, 2, 3, 5, 10, 11, 12, 13]


def test_join_left_taller():
    print("\n================= test_join_left_taller =================")
    # Make left tree clearly taller
    T_left = build_avl_from_list([
        (1, "1"), (2, "2"), (3, "3"), (4, "4"),
        (5, "5"), (6, "6"), (7, "7"), (8, "8")
    ])
    T_right = build_avl_from_list([(20, "20"), (25, "25")])

    print("Left tree (taller):")
    T_left.print_tree()
    print("Right tree (shorter):")
    T_right.print_tree()

    # All keys in left < 15 < all keys in right
    T_left.join(T_right, 15, "15")
    assert check_avl(T_left, "join: left taller")

    keys = [k for (k, _) in T_left.avl_to_array()]
    assert keys == [1, 2, 3, 4, 5, 6, 7, 8, 15, 20, 25]


def test_join_right_taller():
    print("\n================= test_join_right_taller =================")
    # Mirror: right tree taller
    T_left = build_avl_from_list([(1, "1"), (2, "2"), (3, "3")])
    T_right = build_avl_from_list([
        (20, "20"), (21, "21"), (22, "22"),
        (23, "23"), (24, "24"), (25, "25")
    ])

    print("Left tree (shorter):")
    T_left.print_tree()
    print("Right tree (taller):")
    T_right.print_tree()

    # all keys in left < 10 < all keys in right
    T_left.join(T_right, 10, "10")
    assert check_avl(T_left, "join: right taller")
    keys = [k for (k, _) in T_left.avl_to_array()]
    assert keys == [1, 2, 3, 10, 20, 21, 22, 23, 24, 25]


def test_join_chain():
    print("\n================= test_join_chain =================")
    # Chain multiple joins: (((T1 join T2) join T3) join T4)
    T1 = build_avl_from_list([(1, "1"), (2, "2")])
    T2 = build_avl_from_list([(10, "10"), (11, "11")])
    T3 = build_avl_from_list([(20, "20"), (21, "21")])
    T4 = build_avl_from_list([(30, "30"), (31, "31")])

    # T1 keys < 5 < T2 keys
    T1.join(T2, 5, "5")
    check_avl(T1, "after join T1+T2")

    # all keys now < 15 < T3 keys
    T1.join(T3, 15, "15")
    check_avl(T1, "after join (T1+T2)+T3")

    # all keys now < 25 < T4 keys
    T1.join(T4, 25, "25")
    assert check_avl(T1, "after join ((T1+T2)+T3)+T4")

    keys = [k for (k, _) in T1.avl_to_array()]
    assert keys == [1, 2, 5, 10, 11, 15, 20, 21, 25, 30, 31]


def test_join_random_like():
    """
    Not truly random, but “random-like” different shapes and keys.
    Checks:
    - union of keys is correct
    - in-order is sorted
    - AVL invariants hold
    """
    print("\n================= test_join_random_like =================")
    # left side keys
    left_keys = [3, 1, 7, 5, 9, 2]
    right_keys = [40, 50, 45, 42, 60, 55, 48]

    T_left = build_avl_from_list([(k, str(k)) for k in left_keys])
    T_right = build_avl_from_list([(k, str(k)) for k in right_keys])

    # pick separating key between max(left) and min(right)
    sep_key = 20
    T_left.join(T_right, sep_key, str(sep_key))

    assert check_avl(T_left, "join: random-like")

    in_order = T_left.avl_to_array()
    keys = [k for (k, _) in in_order]
    # verify sorted
    assert keys == sorted(left_keys + right_keys + [sep_key])


if __name__ == "__main__":
    # run all tests
    test_join_case_empty_trees()
    test_join_self_empty()
    test_join_tree2_empty()
    test_join_same_height()
    test_join_left_taller()
    test_join_right_taller()
    test_join_chain()
    test_join_random_like()

    print("All join tests finished.")
    
if __name__ == "__main__":

    # ---------- Case 1: same height on both sides ----------
    print("=== Case 1: same height ===")
    A = AVLTree()
    A.insert(10, "10")
    A.insert(5, "5")
    A.insert(15, "15")

    B = AVLTree()
    B.insert(30, "30")
    B.insert(25, "25")
    B.insert(35, "35")

    print("A:")
    A.print_tree()
    print("B:")
    B.print_tree()

    A.join(B, 20, "20")
    print("Joined tree (same height):")
    A.print_tree()
    print("valid height =", A.validate_heights())
    print("valid bf     =", A.validate_balance_factors())

    # ---------- Case 2: left tree taller ----------
    print("\n=== Case 2: left taller ===")
    C = AVLTree()
    for k in [10, 5, 15, 2, 7, 12, 17]:
        C.insert(k, str(k))

    D = AVLTree()
    D.insert(40, "40")

    print("C:")
    C.print_tree()
    print("D:")
    D.print_tree()

    C.join(D, 30, "30")
    print("Joined tree (left taller):")
    C.print_tree()
    print("valid height =", C.validate_heights())
    print("valid bf     =", C.validate_balance_factors())

    # ---------- Case 3: right tree taller ----------
    print("\n=== Case 3: right taller ===")
    E = AVLTree()
    E.insert(5, "5")

    F = AVLTree()
    for k in [20, 10, 30, 8, 12, 25, 35]:
        F.insert(k, str(k))

    print("E:")
    E.print_tree()
    print("F:")
    F.print_tree()

    E.join(F, 9, "9")   # here self is the smaller (left) tree
    print("Joined tree (right taller):")
    E.print_tree()
    print("valid height =", E.validate_heights())
    print("valid bf     =", E.validate_balance_factors())

    # ---------- Case 4: self is the right tree, other is the left tree ----------
    print("\n=== Case 4: self is right tree ===")
    G = AVLTree()
    for k in [20, 10, 30]:
        G.insert(k, str(k))

    H = AVLTree()
    for k in [1, 2, 3]:
        H.insert(k, str(k))

    print("G (right tree):")
    G.print_tree()
    print("H (left tree):")
    H.print_tree()

    # here self (G) has all keys > key, other (H) has all keys < key
    G.join(H, 5, "5")
    print("Joined tree (self was right):")
    G.print_tree()
    print("valid height =", G.validate_heights())
    print("valid bf     =", G.validate_balance_factors())

##if __name__ == "__main__":
##
##    ##regular insertions test
##    T1 = AVLTree()
##    T1.insert(15, "15")
##    T1.insert(10, "10")
##    T1.insert(12, "12")
##    T1.insert(4, "4")
##    T1.insert(11, "11")
##    T1.print_tree()
##    
##    T2 = AVLTree()
##    T2.insert(20, "20")
##    T2.insert(24, "24")
##    T2.insert(26, "26")
##    T2.insert(27, "27")
##    T2.insert(35, "35")
##    T2.insert(31, "31")
##    T2.insert(19, "19")
##    T2.print_tree()
##
##    T1.join(T2, 17, "17")
##
##    print("Tree after join")
##    T1.print_tree()

    ##finger insertions test
##    T2 = AVLTree()
##    T2.finger_insert(15, "15")
##    T2.finger_insert(10, "10")
##    T2.finger_insert(22, "22")
##    T2.finger_insert(4, "4")
##    T2.finger_insert(11, "11")
##    T2.finger_insert(20, "20")
##    T2.finger_insert(24, "24")
##    T2.finger_insert(2, "2")
##    T2.finger_insert(7, "7")
##    T2.finger_insert(12, "12")
##    T2.finger_insert(18, "18")
##    T2.finger_insert(1, "1")
##    T2.finger_insert(6, "6")
##    T2.finger_insert(8, "8")
##    T2.finger_insert(5, "5")
##    T2.print_tree()

    ##other tests
##    print(T.size())
##    print(T.avl_to_array())
##    print(T.get_root().value)
##    print(T.max_node().value)
##    print(T.validate_heights())
##    print(T.validate_balance_factors())
##    T.print_tree()





##if __name__ == "__main__":
##    ##regular insertions test
##    T = AVLTree()
##    T.insert(15, "15")
##    T.insert(10, "10")
##    T.insert(22, "22")
##    T.insert(4, "4")
##    T.insert(11, "11")
##    T.insert(20, "20")
##    T.insert(24, "24")
##    T.insert(2, "2")
##    T.insert(7, "7")
##    T.insert(12, "12")
##    T.insert(18, "18")
##    T.insert(1, "1")
##    T.insert(6, "6")
##    T.insert(8, "8")
##    T.insert(5, "5")
##    T.print_tree()
##    """
##    ##finger insertions test
##    T2 = AVLTree()
##    T2.finger_insert(15, "15")
##    T2.finger_insert(10, "10")
##    T2.finger_insert(22, "22")
##    T2.finger_insert(4, "4")
##    T2.finger_insert(11, "11")
##    T2.finger_insert(20, "20")
##    T2.finger_insert(24, "24")
##    T2.finger_insert(2, "2")
##    T2.finger_insert(7, "7")
##    T2.finger_insert(12, "12")
##    T2.finger_insert(18, "18")
##    T2.finger_insert(1, "1")
##    T2.finger_insert(6, "6")
##    T2.finger_insert(8, "8")
##    T2.finger_insert(5, "5")
##    """
##    #delete test
##    T.print_tree()
##    a,b = T.search(7)
##    T.delete(a)
##    T.print_tree()
##    """
##    ##other tests
##    print(T.size())
##    print(T.avl_to_array())
##    print(T.get_root().value)
##    print(T.max_node().value)
##    print(T.validate_heights())
##    print(T.validate_balance_factors())
##    T.print_tree()
##    """
##    criminal_node.height = criminal_node.height - 2
##    self.set_heights_from_node_up(criminal_node, 'Rotation')
##
##    # ====================================================================
##
##if __name__ == "__main__":
##
##    ##regular insertions test
##    T1 = AVLTree()
##    T1.insert(15, "15")
##    T1.insert(10, "10")
##    T1.insert(12, "12")
##    T1.insert(4, "4")
##    T1.insert(11, "11")
##    T1.print_tree()
##    
##    T2 = AVLTree()
##    T2.insert(20, "20")
##    T2.insert(24, "24")
##    T2.insert(26, "26")
##    T2.insert(27, "27")
##    T2.insert(35, "35")
##    T2.insert(31, "31")
##    T2.print_tree()
##
##    T1.join(T2, 17, "17")

    ##finger insertions test
##    T2 = AVLTree()
##    T2.finger_insert(15, "15")
##    T2.finger_insert(10, "10")
##    T2.finger_insert(22, "22")
##    T2.finger_insert(4, "4")
##    T2.finger_insert(11, "11")
##    T2.finger_insert(20, "20")
##    T2.finger_insert(24, "24")
##    T2.finger_insert(2, "2")
##    T2.finger_insert(7, "7")
##    T2.finger_insert(12, "12")
##    T2.finger_insert(18, "18")
##    T2.finger_insert(1, "1")
##    T2.finger_insert(6, "6")
##    T2.finger_insert(8, "8")
##    T2.finger_insert(5, "5")
##    T2.print_tree()

    ##other tests
##    print(T.size())
##    print(T.avl_to_array())
##    print(T.get_root().value)
##    print(T.max_node().value)
##    print(T.validate_heights())
##    print(T.validate_balance_factors())
##    T.print_tree()

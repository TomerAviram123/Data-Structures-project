# id1:
# name1:
# username1:
# id2:
# name2:
# username2:


"""A class representing a node in an AVL tree"""


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
            return None, 0

        if not node.is_real_node():
            return None, 0

        while node.is_real_node():
            if node.key == key:
                return node, arcs

            elif node.key > key:
                if not node.left.is_real_node():
                    return None, arcs
                else:
                    node = node.left

            elif node.key < key:
                if not node.right.is_real_node():
                    return None, arcs
                else:
                    node = node.right
            arcs += 1

        return None, arcs

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

        # ======== Traverse Up ======================
        while node != self.root:
            if node.key == key:
                return node, arcs
            if key <= node.parent.key:
                node = node.parent
            else:
                break
            arcs += 1

        # ======== Traverse down ======================
        while node is not None and node.is_real_node():
            if node.key == key:
                return node, arcs
            elif node.key > key:
                if not node.left.is_real_node():
                    return None, arcs
                else:
                    node = node.left
            elif node.key < key:
                if not node.right.is_real_node():
                    return None, arcs
                else:
                    node = node.right
            arcs += 1

        return None, arcs

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

        # simple insertion
        x, e = self.simple_insert(self.root, key, val)

        # remember the original route and the heights
        original_route, original_heights = [], {}
        iter_node = x.parent
        while iter_node is not None:
            original_route += [iter_node]
            original_heights[iter_node] = iter_node.height
            iter_node = iter_node.parent

        # update heights
        self.set_heights_from_node_up(x)

        # remember the heights after the updating
        updated_heights = {}
        for node in original_route:
            updated_heights[node] = node.height

        # update tree max, size
        self._size += 1
        if self._max_node is None or self._max_node.key < x.key:
            self._max_node = x

        # Balance Tree
        criminal_node = self.tree_balancer(x, "One Balance")

        # compare original heights to the new heights
        h = 0
        if criminal_node is None:
            route_to_check_for_promotions = original_route
        else:
            route_to_check_for_promotions = original_route[: original_route.index(criminal_node)]
        for node in route_to_check_for_promotions:
            if original_heights[node] < updated_heights[node]:
                h += 1

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
            node = self._max_node
            while node != self.root:
                if key < node.parent.key:
                    node = node.parent
                    arcs += 1
                else:
                    break

        # Simple insert from the common node
        x, e = self.simple_insert(node, key, val)
        e += arcs

        # remember the original route and the heights
        original_route, original_heights = [], {}
        iter_node = x.parent
        while iter_node is not None:
            original_route += [iter_node]
            original_heights[iter_node] = iter_node.height
            iter_node = iter_node.parent

        # update heights
        self.set_heights_from_node_up(x)

        # remember the heights after the updating
        updated_heights = {}
        for node in original_route:
            updated_heights[node] = node.height

        # update tree max, size
        self._size += 1
        if self._max_node is None or self._max_node.key < x.key:
            self._max_node = x

        # Balance Tree
        criminal_node = self.tree_balancer(x, "One Balance")

        # compare original heights to the new heights
        h = 0
        if criminal_node is None:
            route_to_check_for_promotions = original_route
        else:
            route_to_check_for_promotions = original_route[: original_route.index(criminal_node)]
        for node in route_to_check_for_promotions:
            if original_heights[node] < updated_heights[node]:
                h += 1

        return x, e, h

    def delete(self, node):
        """deletes node from the dictionary

        @type node: AVLNode
        @pre: node is a real pointer to a node in self
        """
        # Simple Delete of the node
        y, original_y_parent = self.simple_delete(node)

        # balance Tree
        if original_y_parent is not node:
            start_node = original_y_parent
        else:
            start_node = y

        self.tree_balancer(start_node)

        # update tree max, size
        self._size -= 1
        # if self._max_node == node and self.root is not None:
        if self._max_node == node and self.root is not None:
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
            new_root.parent = None
            self.root = new_root
            self._size = 1
            self._max_node = new_root
            return

        if self.root is None:
            # build result on top of tree2 and copy it into self
            tree2.insert(key, val)
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
            new_node.parent = None

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
        left_tree = AVLTree()
        right_tree = AVLTree()

        if node.left.is_real_node():
            left_tree.root = node.left
            node.left.parent = None
        if node.right.is_real_node():
            right_tree.root = node.right
            node.right.parent = None
        for tree in [left_tree, right_tree]:
            max_node = tree.root
            if tree.root is not None:
                while max_node.right.is_real_node():
                    max_node = max_node.right
            tree._max_node = max_node

        current = node

        while current.parent is not None:
            parent = current.parent
            key = parent.key
            val = parent.value
            temp_tree = AVLTree()

            # Went Left
            if parent.right is current:
                if parent.left.is_real_node():
                    temp_tree.root = parent.left
                    parent.left.parent = None

                    # Find max
                    max_node = temp_tree.root
                    while max_node.right.is_real_node():
                        max_node = max_node.right
                    temp_tree._max_node = max_node

                    left_tree.join(temp_tree, key, val)
                else:
                    left_tree.insert(key, val)
            else:  # Went Right
                if parent.right.is_real_node():
                    temp_tree.root = parent.right
                    parent.right.parent = None

                    # Find max
                    max_node = temp_tree.root
                    while max_node.right.is_real_node():
                        max_node = max_node.right
                    temp_tree._max_node = max_node

                    right_tree.join(temp_tree, key, val)
                else:
                    right_tree.insert(key, val)

            current = parent

        return left_tree, right_tree

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

    def _create_in_order_list(self, x, lst=None):
        if not x or not x.is_real_node():
            return
        self._create_in_order_list(x.left, lst)
        lst.append((x.key, x.value))
        self._create_in_order_list(x.right, lst)

    def tree_balancer(self, start_node, arg="Default"):

        criminal_node = start_node
        continue_ = True
        node_to_return = None

        while criminal_node is not None and criminal_node.is_real_node() and continue_:

            criminal_node_bf = criminal_node.left.height - criminal_node.right.height

            if abs(criminal_node_bf) == 2:  # found the place to do the balance

                node_to_return = criminal_node

                if arg == "One Balance":
                    continue_ = False

                if criminal_node_bf == -2:  # check the right son

                    child_node = criminal_node.right
                    child_node_bf = child_node.left.height - child_node.right.height

                    if child_node_bf in [-1, 0]:  # left rotation
                        self.left_rotation(criminal_node, child_node)

                    elif child_node_bf == 1:  # right then left rotation
                        grandchild_node = child_node.left
                        self.right_then_left_rotation(criminal_node, child_node, grandchild_node)

                elif criminal_node_bf == 2:  # check the left son

                    child_node = criminal_node.left
                    child_node_bf = child_node.left.height - child_node.right.height

                    if child_node_bf in [0, -1]:  # right then left rotation

                        grandchild_node = child_node.right
                        self.left_then_right_rotation(criminal_node, child_node, grandchild_node)

                    elif child_node_bf == 1:  # right rotation

                        self.right_rotation(criminal_node, child_node)

            criminal_node = criminal_node.parent

        return node_to_return

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

        # CASE 1: Node is a leaf
        if not node.left.is_real_node() and not node.right.is_real_node():
            if node == self.root:
                self.root = None
                return self.virtual_node, None

            parent = node.parent
            if parent.left == node:
                parent.left = self.virtual_node
            else:
                parent.right = self.virtual_node

            self.set_heights_from_node_up(parent)
            return parent, parent

        # CASE 2: Node has only right child
        elif node.right.is_real_node() and not node.left.is_real_node():
            if node == self.root:
                self.root = node.right
                node.right.parent = None
                return node.right, None

            parent = node.parent
            if parent.left == node:
                parent.left = node.right
            else:
                parent.right = node.right
            node.right.parent = parent

            self.set_heights_from_node_up(parent)
            return parent, parent

        # CASE 3: Node has only left child
        elif node.left.is_real_node() and not node.right.is_real_node():
            if node == self.root:
                self.root = node.left
                node.left.parent = None
                return node.left, None

            parent = node.parent
            if parent.left == node:
                parent.left = node.left
            else:
                parent.right = node.left
            node.left.parent = parent

            self.set_heights_from_node_up(parent)
            return parent, parent

        # CASE 4: Node has two children
        else:
            successor = node.right
            while successor.left.is_real_node():
                successor = successor.left

            successor_parent = successor.parent

            # If successor is the direct right child of node
            if successor == node.right:
                if node == self.root:
                    self.root = successor
                    successor.parent = None
                else:
                    if node.parent.left == node:
                        node.parent.left = successor
                    else:
                        node.parent.right = successor
                    successor.parent = node.parent

                successor.left = node.left
                if node.left.is_real_node():
                    node.left.parent = successor

                self.set_heights_from_node_up(successor)
                return successor, successor

            # Successor is deeper in the tree
            else:
                # Unlink successor from its parent
                successor_parent.left = successor.right
                if successor.right.is_real_node():
                    successor.right.parent = successor_parent

                # Replace node with successor
                if node == self.root:
                    self.root = successor
                    successor.parent = None
                else:
                    if node.parent.left == node:
                        node.parent.left = successor
                    else:
                        node.parent.right = successor
                    successor.parent = node.parent

                # Successor takes node's children
                successor.left = node.left
                successor.right = node.right
                if node.left.is_real_node():
                    node.left.parent = successor
                if node.right.is_real_node():
                    node.right.parent = successor

                self.set_heights_from_node_up(successor_parent)
                return successor, successor_parent

    # ==================== HELPER ROTATION FUNCTIONS ==================================

    def left_rotation(self, criminal_node, child_node):

        if criminal_node is self.root:
            self.root = child_node
            child_node.parent = None

        else:  # Update parent's pointer to the rotated subtree
            if criminal_node.parent.left == criminal_node:
                criminal_node.parent.left = child_node
            else:
                criminal_node.parent.right = child_node
            child_node.parent = criminal_node.parent

        criminal_node.right = child_node.left
        if criminal_node.right.is_real_node():
            criminal_node.right.parent = criminal_node

        child_node.left = criminal_node
        criminal_node.parent = child_node

        self.set_heights_from_node_up(criminal_node)

        return

    def right_then_left_rotation(self, criminal_node, child_node, grandchild_node):

        if criminal_node is self.root:
            self.root = grandchild_node
            grandchild_node.parent = None
        else:  # Update parent's pointer to the rotated subtree
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

        grandchild_node.left = criminal_node
        grandchild_node.right = child_node

        criminal_node.parent = grandchild_node
        child_node.parent = grandchild_node

        self.set_heights_from_node_up(criminal_node)
        self.set_heights_from_node_up(child_node)

        return

    def left_then_right_rotation(self, criminal_node, child_node, grandchild_node):

        if criminal_node is self.root:
            self.root = grandchild_node
            grandchild_node.parent = None
        else:  # Update parent's pointer to the rotated subtree
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

        self.set_heights_from_node_up(criminal_node)
        self.set_heights_from_node_up(child_node)

        return

    def right_rotation(self, criminal_node, child_node):

        if criminal_node is self.root:
            self.root = child_node
            child_node.parent = None
        else:  # Update parent's pointer to the rotated subtree
            if criminal_node.parent.left == criminal_node:
                criminal_node.parent.left = child_node
            else:
                criminal_node.parent.right = child_node
            child_node.parent = criminal_node.parent

        criminal_node.left = child_node.right
        if criminal_node.left.is_real_node():
            criminal_node.left.parent = criminal_node
        child_node.right = criminal_node
        criminal_node.parent = child_node

        self.set_heights_from_node_up(criminal_node)

        return

    # ====================================================================

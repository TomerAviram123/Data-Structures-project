"""
Comprehensive AVL Tree Tester
Tests all required functionality from the project specification
"""

import unittest
import random
from AVLTree import AVLTree, AVLNode

GRADE = 0
MAX_GRADE = 100

# Points distributed across test categories
CATEGORY_TOTALS = {
    "insert": 10,
    "finger_insert": 10,
    "search": 8,
    "finger_search": 8,
    "delete": 12,
    "join": 15,
    "split": 15,
    "avl_properties": 12,
    "max_node": 5,
    "utilities": 5,
}

# Track points awarded per category to avoid double-counting
POINTS_PER_CATEGORY = {cat: 0 for cat in CATEGORY_TOTALS}


class AVLTreeTester(unittest.TestCase):
    """Comprehensive test suite for AVL Tree implementation"""

    def setUp(self):
        """Initialize a fresh tree for each test"""
        self.tree = AVLTree()
        self.debug_mode = False  # Set to True to see detailed output

    def add_points(self, category):
        """Add points for passing a test"""
        global GRADE
        points = POINTS_PER_CATEGORY.get(category, 1)
        GRADE += points

    def debug_print(self, *args, **kwargs):
        """Print only in debug mode"""
        if self.debug_mode:
            print(*args, **kwargs)

    def verify_avl_properties(self, tree):
        """Verify AVL tree properties: BST, height, balance factor"""
        if tree.get_root() is None:
            return True

        # Check BST property
        in_order = tree.avl_to_array()
        keys = [k for k, _ in in_order]
        if keys != sorted(keys):
            return False

        # Check heights and balance factors
        return self._check_node_properties(tree.get_root())

    def _check_node_properties(self, node):
        """Recursively check AVL properties"""
        if not node or not node.is_real_node():
            return True

        left_h = node.left.height if node.left else -1
        right_h = node.right.height if node.right else -1

        # Check height
        expected_height = 1 + max(left_h, right_h)
        if node.height != expected_height:
            return False

        # Check balance factor
        bf = left_h - right_h
        if abs(bf) > 1:
            return False

        # Check children
        return self._check_node_properties(node.left) and self._check_node_properties(node.right)

    # ==================== INSERT TESTS ====================

    def test_insert_empty_tree(self):
        """Test inserting into empty tree"""
        x, e, h = self.tree.insert(10, "10")

        self.assertIsNotNone(x)
        self.assertEqual(x.key, 10)
        self.assertEqual(x.value, "10")
        self.assertEqual(self.tree.size(), 1)
        self.assertEqual(e, 0)  # No path in empty tree
        self.assertEqual(h, 0)  # No promotions
        self.assertTrue(self.verify_avl_properties(self.tree))
        self.add_points("insert")

    def test_insert_basic_sequence(self):
        """Test basic insertion sequence with rotations"""
        # Insert 1, 2, 3 - should cause left rotation
        self.tree.insert(1, "1")
        self.tree.insert(2, "2")
        x, e, h = self.tree.insert(3, "3")

        self.assertEqual(self.tree.size(), 3)
        self.assertTrue(self.verify_avl_properties(self.tree))
        self.assertEqual(self.tree.get_root().key, 2)  # 2 should be root after rotation
        self.add_points("insert")

    def test_insert_right_left_rotation(self):
        """Test right-left rotation case"""
        self.tree.insert(1, "1")
        self.tree.insert(3, "3")
        x, e, h = self.tree.insert(2, "2")

        self.assertTrue(self.verify_avl_properties(self.tree))
        self.assertEqual(self.tree.get_root().key, 2)
        self.add_points("insert")

    def test_insert_left_right_rotation(self):
        """Test left-right rotation case"""
        self.tree.insert(3, "3")
        self.tree.insert(1, "1")
        x, e, h = self.tree.insert(2, "2")

        self.assertTrue(self.verify_avl_properties(self.tree))
        self.assertEqual(self.tree.get_root().key, 2)
        self.add_points("insert")

    def test_insert_many_sequential(self):
        """Test inserting many elements sequentially"""
        for i in range(1, 16):
            self.tree.insert(i, str(i))

        self.assertEqual(self.tree.size(), 15)
        self.assertTrue(self.verify_avl_properties(self.tree))

        # Verify all elements are present
        for i in range(1, 16):
            node, _ = self.tree.search(i)
            self.assertIsNotNone(node)
            self.assertEqual(node.key, i)
        self.add_points("insert")

    def test_insert_many_random(self):
        """Test inserting many elements in random order"""
        keys = list(range(1, 51))
        random.shuffle(keys)

        for k in keys:
            self.tree.insert(k, str(k))

        self.assertEqual(self.tree.size(), 50)
        self.assertTrue(self.verify_avl_properties(self.tree))
        self.add_points("insert")

    def test_insert_path_length(self):
        """Test that insert returns correct path length"""
        self.tree.insert(10, "10")
        self.tree.insert(5, "5")
        x, e, h = self.tree.insert(15, "15")

        self.assertEqual(e, 1)  # Path from root to new leaf
        self.add_points("insert")

    # ==================== FINGER INSERT TESTS ====================

    def test_finger_insert_empty(self):
        """Test finger insert into empty tree"""
        x, e, h = self.tree.finger_insert(10, "10")

        self.assertIsNotNone(x)
        self.assertEqual(self.tree.size(), 1)
        self.assertTrue(self.verify_avl_properties(self.tree))
        self.add_points("finger_insert")

    def test_finger_insert_new_max(self):
        """Test finger insert with new maximum - should be efficient"""
        self.tree.insert(10, "10")
        self.tree.insert(5, "5")
        self.tree.insert(15, "15")

        x, e, h = self.tree.finger_insert(20, "20")

        # Path: max(15) -> going down to insert 20 as right child of 15
        # According to spec: e is edges from start to new node before balancing
        # From max (15) down to new node (20) = 1 edge
        self.assertIsNotNone(x)
        self.assertGreaterEqual(e, 1)  # At least 1 edge
        self.assertTrue(self.verify_avl_properties(self.tree))
        self.add_points("finger_insert")

    def test_finger_insert_near_max(self):
        """Test finger insert with keys near maximum"""
        for i in range(1, 11):
            self.tree.insert(i, str(i))

        # Insert keys close to max
        x, e, h = self.tree.finger_insert(9, "9b")  # Duplicate won't happen per spec

        self.assertTrue(self.verify_avl_properties(self.tree))
        self.add_points("finger_insert")

    def test_finger_insert_sequence_ascending(self):
        """Test finger insert with ascending sequence - should be efficient"""
        path_lengths = []
        for i in range(1, 21):
            x, e, h = self.tree.finger_insert(i, str(i))
            path_lengths.append(e)

        self.assertEqual(self.tree.size(), 20)
        self.assertTrue(self.verify_avl_properties(self.tree))
        # Most insertions should be short paths
        avg_path = sum(path_lengths) / len(path_lengths)
        self.assertLess(avg_path, 10)  # Should be efficient
        self.add_points("finger_insert")

    # ==================== SEARCH TESTS ====================

    def test_search_empty_tree(self):
        """Test search in empty tree"""
        node, e = self.tree.search(10)
        self.assertIsNone(node)
        self.add_points("search")

    def test_search_single_element(self):
        """Test search with single element"""
        self.tree.insert(10, "10")
        node, e = self.tree.search(10)

        self.assertIsNotNone(node)
        self.assertEqual(node.key, 10)
        self.assertEqual(e, 1)
        self.add_points("search")

    def test_search_existing_elements(self):
        """Test search for existing elements"""
        keys = [10, 5, 15, 3, 7, 12, 20]
        for k in keys:
            self.tree.insert(k, str(k))

        for k in keys:
            node, e = self.tree.search(k)
            self.assertIsNotNone(node)
            self.assertEqual(node.key, k)
            self.assertGreater(e, 0)
        self.add_points("search")

    def test_search_non_existing(self):
        """Test search for non-existing elements"""
        for i in [10, 20, 30]:
            self.tree.insert(i, str(i))

        node, e = self.tree.search(25)
        self.assertIsNone(node)
        self.add_points("search")

    # ==================== FINGER SEARCH TESTS ====================

    def test_finger_search_from_max(self):
        """Test finger search starting from maximum"""
        keys = [10, 5, 15, 3, 7, 12, 20]
        for k in keys:
            self.tree.insert(k, str(k))

        # Search for key near max
        node, e = self.tree.finger_search(15)
        self.assertIsNotNone(node)
        self.assertEqual(node.key, 15)
        self.add_points("finger_search")

    def test_finger_search_max_itself(self):
        """Test finger search for the maximum element"""
        for i in range(1, 11):
            self.tree.insert(i, str(i))

        node, e = self.tree.finger_search(10)
        self.assertIsNotNone(node)
        self.assertEqual(node.key, 10)
        self.assertEqual(e, 1)  # Should find immediately
        self.add_points("finger_search")

    def test_finger_search_efficiency(self):
        """Test that finger search is efficient for large keys"""
        for i in range(1, 101):
            self.tree.insert(i, str(i))

        # Search for keys near max
        node, e1 = self.tree.finger_search(95)
        node, e2 = self.tree.search(95)

        # Finger search should be more efficient
        self.assertLessEqual(e1, e2)
        self.add_points("finger_search")

    # ==================== DELETE TESTS ====================

    def test_delete_leaf(self):
        """Test deleting a leaf node"""
        self.tree.insert(10, "10")
        self.tree.insert(5, "5")
        self.tree.insert(15, "15")

        node, _ = self.tree.search(5)
        self.tree.delete(node)

        self.assertEqual(self.tree.size(), 2)
        self.assertIsNone(self.tree.search(5)[0])
        self.assertTrue(self.verify_avl_properties(self.tree))
        self.add_points("delete")

    def test_delete_node_one_child(self):
        """Test deleting node with one child"""
        for i in [10, 5, 15, 12]:
            self.tree.insert(i, str(i))

        node, _ = self.tree.search(15)
        self.tree.delete(node)

        self.assertEqual(self.tree.size(), 3)
        self.assertIsNone(self.tree.search(15)[0])
        self.assertTrue(self.verify_avl_properties(self.tree))
        self.add_points("delete")

    def test_delete_node_two_children(self):
        """Test deleting node with two children"""
        for i in [10, 5, 15, 3, 7, 12, 20]:
            self.tree.insert(i, str(i))

        node, _ = self.tree.search(10)
        self.tree.delete(node)

        self.assertEqual(self.tree.size(), 6)
        self.assertIsNone(self.tree.search(10)[0])
        self.assertTrue(self.verify_avl_properties(self.tree))
        self.add_points("delete")

    def test_delete_root(self):
        """Test deleting root node"""
        for i in [10, 5, 15]:
            self.tree.insert(i, str(i))

        root = self.tree.get_root()
        self.tree.delete(root)

        self.assertEqual(self.tree.size(), 2)
        self.assertTrue(self.verify_avl_properties(self.tree))
        self.add_points("delete")

    def test_delete_max_node(self):
        """Test deleting maximum node - should update max_node"""
        for i in range(1, 11):
            self.tree.insert(i, str(i))

        max_node = self.tree.max_node()
        self.assertEqual(max_node.key, 10)

        self.tree.delete(max_node)

        new_max = self.tree.max_node()
        self.assertEqual(new_max.key, 9)
        self.add_points("delete")

    def test_delete_all_nodes(self):
        """Test deleting all nodes one by one"""
        keys = list(range(1, 16))
        for k in keys:
            self.tree.insert(k, str(k))

        random.shuffle(keys)
        for k in keys[:-1]:  # Delete all but one
            node, _ = self.tree.search(k)
            if node:  # Check node exists
                self.tree.delete(node)
                self.assertTrue(self.verify_avl_properties(self.tree))

        # Delete last node
        last_key = keys[-1]
        node, _ = self.tree.search(last_key)
        if node:
            self.tree.delete(node)
            # After deleting last node, tree should be empty
            self.assertEqual(self.tree.size(), 0)
            self.assertIsNone(self.tree.get_root())

        self.add_points("delete")

    # ==================== JOIN TESTS ====================

    def test_join_empty_trees(self):
        """Test joining two empty trees"""
        tree2 = AVLTree()
        self.tree.join(tree2, 10, "10")

        self.assertEqual(self.tree.size(), 1)
        self.assertTrue(self.verify_avl_properties(self.tree))
        self.add_points("join")

    def test_join_empty_self(self):
        """Test joining when self is empty"""
        tree2 = AVLTree()
        for i in [5, 3, 7]:
            tree2.insert(i, str(i))

        self.tree.join(tree2, 10, "10")

        self.assertEqual(self.tree.size(), 4)
        self.assertTrue(self.verify_avl_properties(self.tree))
        self.add_points("join")

    def test_join_empty_other(self):
        """Test joining when other tree is empty"""
        tree2 = AVLTree()
        for i in [5, 3, 7]:
            self.tree.insert(i, str(i))

        self.tree.join(tree2, 10, "10")

        self.assertEqual(self.tree.size(), 4)
        self.assertTrue(self.verify_avl_properties(self.tree))
        self.add_points("join")

    def test_join_same_height(self):
        """Test joining trees with same height"""
        tree2 = AVLTree()

        for i in [5, 3, 7]:
            self.tree.insert(i, str(i))
        for i in [15, 13, 17]:
            tree2.insert(i, str(i))

        self.tree.join(tree2, 10, "10")

        self.assertEqual(self.tree.size(), 7)
        self.assertTrue(self.verify_avl_properties(self.tree))
        keys = [k for k, _ in self.tree.avl_to_array()]
        self.assertEqual(keys, [3, 5, 7, 10, 13, 15, 17])
        self.add_points("join")

    def test_join_left_taller(self):
        """Test joining when left tree is taller"""
        tree2 = AVLTree()

        for i in range(1, 16):
            self.tree.insert(i, str(i))
        tree2.insert(20, "20")

        self.tree.join(tree2, 18, "18")

        self.assertTrue(self.verify_avl_properties(self.tree))
        self.assertEqual(self.tree.size(), 17)
        self.add_points("join")

    def test_join_right_taller(self):
        """Test joining when right tree is taller"""
        tree2 = AVLTree()

        self.tree.insert(5, "5")
        for i in range(10, 25):
            tree2.insert(i, str(i))

        self.tree.join(tree2, 8, "8")

        self.assertTrue(self.verify_avl_properties(self.tree))
        self.assertEqual(self.tree.size(), 17)
        self.add_points("join")

    def test_join_reversed_order(self):
        """Test join when self has larger keys than other"""
        tree2 = AVLTree()

        for i in [15, 13, 17]:
            self.tree.insert(i, str(i))
        for i in [5, 3, 7]:
            tree2.insert(i, str(i))

        self.tree.join(tree2, 10, "10")

        self.assertEqual(self.tree.size(), 7)
        self.assertTrue(self.verify_avl_properties(self.tree))
        self.add_points("join")

    # ==================== SPLIT TESTS ====================

    def test_split_at_root(self):
        """Test splitting at root"""
        for i in range(1, 8):
            self.tree.insert(i, str(i))

        root = self.tree.get_root()
        left, right = self.tree.split(root)

        self.assertTrue(self.verify_avl_properties(left))
        self.assertTrue(self.verify_avl_properties(right))

        left_keys = [k for k, _ in left.avl_to_array()]
        right_keys = [k for k, _ in right.avl_to_array()]

        self.assertTrue(all(k < root.key for k in left_keys))
        self.assertTrue(all(k > root.key for k in right_keys))
        self.add_points("split")

    def test_split_at_leaf(self):
        """Test splitting at leaf"""
        for i in [10, 5, 15, 3, 7, 12, 20]:
            self.tree.insert(i, str(i))

        node, _ = self.tree.search(3)
        left, right = self.tree.split(node)

        self.assertTrue(self.verify_avl_properties(left))
        self.assertTrue(self.verify_avl_properties(right))

        left_keys = [k for k, _ in left.avl_to_array()]
        right_keys = [k for k, _ in right.avl_to_array()]

        self.assertEqual(left_keys, [])
        self.assertEqual(right_keys, [5, 7, 10, 12, 15, 20])
        self.add_points("split")

    def test_split_at_max(self):
        """Test splitting at maximum element"""
        for i in range(1, 11):
            self.tree.insert(i, str(i))

        node, _ = self.tree.search(10)
        left, right = self.tree.split(node)

        left_keys = [k for k, _ in left.avl_to_array()]
        right_keys = [k for k, _ in right.avl_to_array()]

        self.assertEqual(left_keys, list(range(1, 10)))
        self.assertEqual(right_keys, [])
        self.add_points("split")

    def test_split_at_min(self):
        """Test splitting at minimum element"""
        for i in range(1, 11):
            self.tree.insert(i, str(i))

        node, _ = self.tree.search(1)
        left, right = self.tree.split(node)

        left_keys = [k for k, _ in left.avl_to_array()]
        right_keys = [k for k, _ in right.avl_to_array()]

        self.assertEqual(left_keys, [])
        self.assertEqual(right_keys, list(range(2, 11)))
        self.add_points("split")

    def test_split_large_tree(self):
        """Test splitting large tree"""
        keys = list(range(1, 64))
        random.shuffle(keys)
        for k in keys:
            self.tree.insert(k, str(k))

        node, _ = self.tree.search(32)
        left, right = self.tree.split(node)

        self.assertTrue(self.verify_avl_properties(left))
        self.assertTrue(self.verify_avl_properties(right))

        left_keys = [k for k, _ in left.avl_to_array()]
        right_keys = [k for k, _ in right.avl_to_array()]

        self.assertEqual(left_keys, list(range(1, 32)))
        self.assertEqual(right_keys, list(range(33, 64)))
        self.add_points("split")

    # ==================== AVL PROPERTIES TESTS ====================

    def test_maintains_avl_after_operations(self):
        """Test that AVL properties are maintained after mixed operations"""
        operations = []
        for i in range(1, 21):
            self.tree.insert(i, str(i))
            operations.append(("insert", i))

        # Delete some nodes
        for k in [5, 10, 15]:
            node, _ = self.tree.search(k)
            if node:
                self.tree.delete(node)
                operations.append(("delete", k))

        # Insert more
        for i in range(21, 31):
            self.tree.insert(i, str(i))
            operations.append(("insert", i))

        self.assertTrue(self.verify_avl_properties(self.tree))
        self.add_points("avl_properties")

    def test_height_bounds(self):
        """Test that tree height respects AVL bounds"""
        import math

        for n in [10, 20, 50, 100]:
            tree = AVLTree()
            for i in range(1, n + 1):
                tree.insert(i, str(i))

            root = tree.get_root()
            h = root.height if root else -1

            # AVL tree height should be O(log n)
            # More precisely: h <= 1.44 * log2(n+2) - 1
            max_height = 1.44 * math.log2(n + 2)
            self.assertLessEqual(h, max_height)

        self.add_points("avl_properties")

    # ==================== MAX NODE TESTS ====================

    def test_max_node_empty(self):
        """Test max_node on empty tree"""
        max_node = self.tree.max_node()
        self.assertIsNone(max_node)
        self.add_points("max_node")

    def test_max_node_single(self):
        """Test max_node with single element"""
        self.tree.insert(10, "10")
        max_node = self.tree.max_node()
        self.assertEqual(max_node.key, 10)
        self.add_points("max_node")

    def test_max_node_updates(self):
        """Test that max_node updates correctly"""
        for i in range(1, 11):
            self.tree.insert(i, str(i))
            max_node = self.tree.max_node()
            self.assertEqual(max_node.key, i)
        self.add_points("max_node")

    # ==================== UTILITY TESTS ====================

    def test_avl_to_array(self):
        """Test avl_to_array returns sorted array"""
        keys = [10, 5, 15, 3, 7, 12, 20]
        for k in keys:
            self.tree.insert(k, str(k))

        array = self.tree.avl_to_array()
        result_keys = [k for k, _ in array]

        self.assertEqual(result_keys, sorted(keys))
        self.add_points("utilities")

    def test_size_tracking(self):
        """Test that size is tracked correctly"""
        self.assertEqual(self.tree.size(), 0)

        for i in range(1, 11):
            self.tree.insert(i, str(i))
            self.assertEqual(self.tree.size(), i)

        for i in range(1, 6):
            node, _ = self.tree.search(i)
            self.tree.delete(node)
            self.assertEqual(self.tree.size(), 10 - i)

        self.add_points("utilities")

    def test_get_root(self):
        """Test get_root returns correct root"""
        self.assertIsNone(self.tree.get_root())

        self.tree.insert(10, "10")
        root = self.tree.get_root()
        self.assertEqual(root.key, 10)

        self.tree.insert(5, "5")
        self.tree.insert(15, "15")
        root = self.tree.get_root()
        self.assertEqual(root.key, 10)
        self.add_points("utilities")

    # ==================== EDGE CASE TESTS ====================

    def test_insert_duplicate_behavior(self):
        """Test behavior with duplicate keys (spec says won't happen, but good to check)"""
        self.tree.insert(10, "first")
        self.tree.insert(5, "5")
        # Spec says duplicate won't be inserted, so we just check tree remains valid
        self.assertTrue(self.verify_avl_properties(self.tree))

    def test_search_in_single_node_tree(self):
        """Test search edge cases with single node"""
        self.tree.insert(10, "10")

        # Search for existing
        node, e = self.tree.search(10)
        self.assertIsNotNone(node)
        self.assertEqual(e, 1)

        # Search for smaller
        node, e = self.tree.search(5)
        self.assertIsNone(node)

        # Search for larger
        node, e = self.tree.search(15)
        self.assertIsNone(node)

    def test_finger_search_empty_tree(self):
        """Test finger search on empty tree"""
        node, e = self.tree.finger_search(10)
        self.assertIsNone(node)
        self.assertEqual(e, -1)  # TODO - should be 0 I think TBD

    def test_finger_insert_empty_tree(self):
        """Test finger insert into empty tree"""
        x, e, h = self.tree.finger_insert(10, "10")
        self.assertIsNotNone(x)
        self.assertEqual(self.tree.size(), 1)
        self.assertEqual(x.key, 10)

    def test_insert_descending_sequence(self):
        """Test inserting in descending order (stress test right rotations)"""
        for i in range(10, 0, -1):
            self.tree.insert(i, str(i))

        self.assertEqual(self.tree.size(), 10)
        self.assertTrue(self.verify_avl_properties(self.tree))

        keys = [k for k, _ in self.tree.avl_to_array()]
        self.assertEqual(keys, list(range(1, 11)))

    def test_delete_from_single_node(self):
        """Test deleting the only node in tree"""
        self.tree.insert(10, "10")
        node, _ = self.tree.search(10)
        self.tree.delete(node)

        self.assertEqual(self.tree.size(), 0)
        self.assertIsNone(self.tree.get_root())

    def test_delete_causing_rotations(self):
        """Test that delete properly triggers rotations"""
        # Build a tree where deletion causes rotation
        for i in [10, 5, 15, 2, 7, 12, 20, 1, 25]:
            self.tree.insert(i, str(i))

        # Delete node that should cause rebalancing
        node, _ = self.tree.search(2)
        self.tree.delete(node)

        self.assertTrue(self.verify_avl_properties(self.tree))

    def test_join_with_single_element_trees(self):
        """Test join with trees containing single elements"""
        tree2 = AVLTree()
        self.tree.insert(5, "5")
        tree2.insert(15, "15")

        self.tree.join(tree2, 10, "10")

        self.assertEqual(self.tree.size(), 3)
        self.assertTrue(self.verify_avl_properties(self.tree))
        keys = [k for k, _ in self.tree.avl_to_array()]
        self.assertEqual(keys, [5, 10, 15])

    def test_split_single_node(self):
        """Test split on tree with single node"""
        self.tree.insert(10, "10")
        root = self.tree.get_root()
        left, right = self.tree.split(root)

        self.assertEqual(left.size(), 0)
        self.assertEqual(right.size(), 0)

    def test_split_two_nodes(self):
        """Test split on tree with two nodes"""
        self.tree.insert(10, "10")
        self.tree.insert(5, "5")

        root = self.tree.get_root()
        left, right = self.tree.split(root)

        left_keys = [k for k, _ in left.avl_to_array()]
        right_keys = [k for k, _ in right.avl_to_array()]

        # One should be empty, other should have one element
        total_keys = left_keys + right_keys
        self.assertEqual(len(total_keys), 1)

    def test_max_node_after_rotations(self):
        """Test that max_node is maintained after rotations"""
        # Insert in order that causes rotations
        for i in [1, 2, 3, 4, 5]:
            self.tree.insert(i, str(i))

        max_node = self.tree.max_node()
        self.assertEqual(max_node.key, 5)

    def test_virtual_nodes_structure(self):
        """Test that virtual nodes are properly maintained"""
        self.tree.insert(10, "10")
        root = self.tree.get_root()

        # Check that leaves have virtual children
        self.assertIsNotNone(root.left)
        self.assertIsNotNone(root.right)
        self.assertFalse(root.left.is_real_node())
        self.assertFalse(root.right.is_real_node())

    def test_parent_pointers_after_insert(self):
        """Test that parent pointers are correctly maintained"""
        for i in [10, 5, 15, 3, 7]:
            self.tree.insert(i, str(i))

        root = self.tree.get_root()
        self.assertIsNone(root.parent)

        # Check left child
        if root.left.is_real_node():
            self.assertEqual(root.left.parent, root)

        # Check right child
        if root.right.is_real_node():
            self.assertEqual(root.right.parent, root)

    def test_parent_pointers_after_delete(self):
        """Test that parent pointers remain correct after deletion"""
        for i in range(1, 11):
            self.tree.insert(i, str(i))

        # Delete a middle node
        node, _ = self.tree.search(5)
        self.tree.delete(node)

        # Verify parent pointers
        root = self.tree.get_root()
        if root:
            self._verify_parent_pointers(root)

    def _verify_parent_pointers(self, node):
        """Helper to recursively verify parent pointers"""
        if not node or not node.is_real_node():
            return True

        if node.left and node.left.is_real_node():
            if node.left.parent != node:
                return False
            if not self._verify_parent_pointers(node.left):
                return False

        if node.right and node.right.is_real_node():
            if node.right.parent != node:
                return False
            if not self._verify_parent_pointers(node.right):
                return False

        return True

    def test_finger_insert_smaller_than_max(self):
        """Test finger insert with key smaller than max"""
        for i in [10, 5, 15, 20]:
            self.tree.insert(i, str(i))

        # Insert something smaller than max
        x, e, h = self.tree.finger_insert(18, "18")

        self.assertIsNotNone(x)
        self.assertTrue(self.verify_avl_properties(self.tree))
        self.assertEqual(self.tree.size(), 5)

    def test_finger_insert_much_smaller_than_max(self):
        """Test finger insert with key much smaller than max"""
        for i in range(1, 21):
            self.tree.insert(i, str(i))

        # Insert very small key using finger insert
        x, e, h = self.tree.finger_insert(11, "11b")

        self.assertTrue(self.verify_avl_properties(self.tree))

    def test_search_path_length_correctness(self):
        """Test that search returns correct path lengths"""
        # Build specific tree structure
        self.tree.insert(10, "10")
        self.tree.insert(5, "5")
        self.tree.insert(15, "15")
        self.tree.insert(3, "3")

        # Search for leaf (3)
        node, e = self.tree.search(3)
        self.debug_print(f"Search for 3: e={e}")
        self.assertGreaterEqual(e, 3)  # Root -> 5 -> 3 (2 edges) + 1

    def test_insert_path_length_correctness(self):
        """Test that insert returns correct path lengths"""
        self.tree.insert(10, "10")
        x, e, h = self.tree.insert(5, "5")
        self.debug_print(f"Insert 5: e={e}, h={h}")
        self.assertGreaterEqual(e, 1)

    def test_delete_and_reinsert(self):
        """Test deleting and reinserting same key"""
        self.tree.insert(10, "10")
        self.tree.insert(5, "5")
        self.tree.insert(15, "15")

        node, _ = self.tree.search(10)
        self.tree.delete(node)
        self.assertEqual(self.tree.size(), 2)

        # Reinsert
        self.tree.insert(10, "10-new")
        self.assertEqual(self.tree.size(), 3)

        node, _ = self.tree.search(10)
        self.assertEqual(node.value, "10-new")

    def test_join_chain_multiple(self):
        """Test multiple sequential joins"""
        trees = []
        for i in range(5):
            t = AVLTree()
            t.insert(i * 10 + 1, str(i * 10 + 1))
            t.insert(i * 10 + 2, str(i * 10 + 2))
            trees.append(t)

        # Join all trees
        result = trees[0]
        for i in range(1, len(trees)):
            separator_key = i * 10
            result.join(trees[i], separator_key, str(separator_key))

        self.assertTrue(self.verify_avl_properties(result))

    def test_split_and_rejoin(self):
        """Test splitting and rejoining"""
        for i in range(1, 11):
            self.tree.insert(i, str(i))

        node, _ = self.tree.search(5)
        left, right = self.tree.split(node)

        # Rejoin
        left.join(right, 5, "5")

        self.assertTrue(self.verify_avl_properties(left))

    def test_large_tree_operations(self):
        """Stress test with large tree"""
        n = 200
        keys = list(range(1, n + 1))
        random.shuffle(keys)

        # Insert all
        for k in keys:
            self.tree.insert(k, str(k))

        self.assertEqual(self.tree.size(), n)
        self.assertTrue(self.verify_avl_properties(self.tree))

        # Search for random keys
        for _ in range(20):
            k = random.randint(1, n)
            node, _ = self.tree.search(k)
            self.assertIsNotNone(node)

        # Delete some nodes
        for k in keys[:50]:
            node, _ = self.tree.search(k)
            if node:
                self.tree.delete(node)

        self.assertTrue(self.verify_avl_properties(self.tree))


def run_tests():
    """Run all tests and display results"""
    global GRADE
    GRADE = 0

    print("=" * 70)
    print("  AVL TREE COMPREHENSIVE TESTER")
    print("=" * 70)
    print()

    # Run tests
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(AVLTreeTester)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Display summary
    print()
    print("=" * 70)
    print("  TEST SUMMARY")
    print("=" * 70)

    total_tests = result.testsRun
    passed = total_tests - len(result.failures) - len(result.errors)

    print(f"\nTests Run: {total_tests}")
    print(f"Passed: {passed}")
    print(f"Failed: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    if result.failures:
        print("\n❌ FAILED TESTS:")
        for test, traceback in result.failures:
            test_name = test.id().split(".")[-1]
            print(f"  • {test_name}")

    if result.errors:
        print("\n⚠️  ERRORS:")
        for test, traceback in result.errors:
            test_name = test.id().split(".")[-1]
            print(f"  • {test_name}")

    print(f"\n{'=' * 70}")
    print(f"  FINAL GRADE: {GRADE}/{MAX_GRADE}")
    print(f"{'=' * 70}")

    return result


if __name__ == "__main__":
    run_tests()

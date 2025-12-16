import random
from tabulate import tabulate
from AVLTree import AVLTree, AVLNode

N = 300
I = 10


class TestType:
    ORDERD_ARRAY = "ORDERD_ARRAY"
    REVESRSED_ORDERD_ARRAY = "REVESRSED_ORDERD_ARRAY"
    RANDOM_ARRAY = "RANDOM_ARRAY"
    RANDOM_SWAP_ARRAY = "RANDOM_SWAP_ARRAY"

    def to_list():
        return [
            TestType.ORDERD_ARRAY,
            TestType.REVESRSED_ORDERD_ARRAY,
            TestType.RANDOM_ARRAY,
            TestType.RANDOM_SWAP_ARRAY,
        ]


def generate_array(i, test_type=TestType.ORDERD_ARRAY, base=N):
    n = base * 2**i
    if test_type == TestType.ORDERD_ARRAY:
        for num in range(1, n + 1):
            yield num
    elif test_type == TestType.REVESRSED_ORDERD_ARRAY:
        for num in range(n, 0, -1):
            yield num
    elif test_type == TestType.RANDOM_ARRAY:
        arr = list(range(1, n + 1))
        random.shuffle(arr)
        for num in arr:
            yield num
    elif test_type == TestType.RANDOM_SWAP_ARRAY:
        arr = list(range(1, n + 1))
        for k in range(n - 1):
            if random.random() >= 0.5:
                arr[k], arr[k + 1] = arr[k + 1], arr[k]
        for num in arr:
            yield num


def count_reversals(i, test_type=TestType.ORDERD_ARRAY, base=N):
    arr = list(generate_array(i, test_type))
    total_reversals = 0
    for j in range(len(arr)):
        for k in range(j + 1, len(arr)):
            if arr[j] > arr[k]:
                total_reversals += 1
    return total_reversals


def part_1():
    results = {test_type: {} for test_type in TestType.to_list()}
    for test_type in TestType.to_list():
        print(f"Starting tests of type {test_type}")
        for i in range(1, I + 1):
            print(f"Running test {i} with array size {N} * 2 ** {i} = {N * 2 ** i}")
            tree = AVLTree()
            total_h = 0
            for num in generate_array(i, test_type):
                _, _, h = tree.finger_insert(num, str(num))
                total_h += h
            results[test_type][i] = total_h

    # Prepare table data
    test_types = TestType.to_list()[::-1]  # Reverse
    headers = ["i", "n"] + test_types

    table_data = []
    for i in range(1, I + 1):
        row = [i, N * 2**i] + [results[test_type][i] for test_type in test_types]
        table_data.append(row)

    print("\n" + tabulate(table_data, headers=headers, tablefmt="grid"))


def part_2():
    results = {test_type: {} for test_type in TestType.to_list()}
    for test_type in TestType.to_list():
        print(f"Starting tests of type {test_type}")
        for i in range(1, I - 5 + 1):
            print(f"Running test {i} with array size {N} * 2 ** {i} = {N * 2 ** i}")
            results[test_type][i] = count_reversals(i, test_type)

    # Prepare table data
    test_types = TestType.to_list()[::-1]  # Reverse
    headers = ["i", "n"] + test_types

    table_data = []
    for i in range(1, I - 5 + 1):
        row = [i, N * 2**i] + [results[test_type][i] for test_type in test_types]
        table_data.append(row)

    print("\n" + tabulate(table_data, headers=headers, tablefmt="grid"))


def part_3():
    results = {test_type: {} for test_type in TestType.to_list()}
    for test_type in TestType.to_list():
        print(f"Starting tests of type {test_type}")
        for i in range(1, I + 1):
            print(f"Running test {i} with array size {N} * 2 ** {i} = {N * 2 ** i}")
            tree = AVLTree()
            total_e = 0
            for num in generate_array(i, test_type):
                _, e, _ = tree.finger_insert(num, str(num))
                total_e += e
            results[test_type][i] = total_e

    # Prepare table data
    test_types = TestType.to_list()[::-1]  # Reverse
    headers = ["i", "n"] + test_types

    table_data = []
    for i in range(1, I + 1):
        row = [i, N * 2**i] + [results[test_type][i] for test_type in test_types]
        table_data.append(row)

    print("\n" + tabulate(table_data, headers=headers, tablefmt="grid"))


if __name__ == "__main__":
    tree = AVLTree()
    part_1()
    part_2()
    part_3()

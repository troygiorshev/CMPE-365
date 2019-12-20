"""CMPE 365 Lab 10 + 11 / Assignment 4

2019-11-24 (3 Weeks: 12-13)

Troy Giorshev
20012707
15tag2

I certify that this submission contains my own work, except as noted.
(hash_fn)

==Assumptions==

None Needed.

==Other Notes==

python, mypy, yapf, pylint, yapf

The bad hash function in Lab 9 first appeared in K&R (1st ed)!

"""
import sys
from typing import List, Tuple


class SHPair:
    """Class for holding String-Hash pairs"""
    def __init__(self, s: str, h: int) -> None:
        self.s = s
        self.h = h


def hash_fn(s: str) -> int:
    """Hash the string
    I think this is (at least close to, or historically) the hashing algorithm
    that python uses for its dictionaries!
    **Credit to:** <https://stackoverflow.com/questions/8997894/what-hash-algorithm-does-pythons-dictionary-mapping-use>
    Modified slightly
    Apparently it's a version of this:
    <https://en.wikipedia.org/wiki/Fowler%E2%80%93Noll%E2%80%93Vo_hash_function>
    <https://www.python.org/dev/peps/pep-0456/>
    """

    ret = ord(s[0]) << 7
    for c in s[1:]:
        ret = ((1000003 * ret) ^ ord(c)) % (1 << 32)
    return ret


def is_eq(s1: SHPair, s2: SHPair) -> bool:
    """Check if the two string-hash pairs are equal"""
    if s1.h == s2.h:
        return s1.s == s2.s
    else:
        return False


def lcsl(sl1: List[SHPair], sl2: List[SHPair], p1: int, p2: int,
         arr: List[List[int]]) -> int:
    """Longest Common Subsequence Length

    Args:
        sl1:    The list of string-hash pairs of the first file
        sl2:    The list of string-hash pairs of the second file
        p1:     Index of the current string in the first file
        p2:     Index of to the current string in the second file
        arr:    The dynamic programming array
    Returns:
        The Longest Common Subsequence Length of sl1[:p1] and sl2[:p2]
    """

    # Base cases
    if p1 == 0 and p2 == 0:
        return 1 if is_eq(sl1[0], sl2[0]) else 0
    if p1 == 0:
        return 1 if (arr[0][p2 - 1] == 1) or is_eq(sl1[0], sl2[p2]) else 0
    if p2 == 0:
        return 1 if (arr[p1 - 1][0] == 1) or is_eq(sl1[p1], sl2[0]) else 0
    # Real stuff
    if is_eq(sl1[p1], sl2[p2]):
        return 1 + arr[p1 - 1][p2 - 1]
    else:
        return max(arr[p1 - 1][p2], arr[p1][p2 - 1], arr[p1 - 1][p2 - 1])


def fill_table(sl1: List[SHPair], sl2: List[SHPair]) -> List[List[int]]:
    """Create the dynamic programming 2D array
    
    ROW by COL
    """
    arr = [[0 for _ in enumerate(sl2)] for _ in enumerate(sl1)]

    for i, _ in enumerate(sl1):
        for j, _ in enumerate(sl2):
            arr[i][j] = lcsl(sl1, sl2, i, j, arr)

    return (arr)


def traverse_table(sl1: List[SHPair], sl2: List[SHPair],
                   arr: List[List[int]]) -> Tuple[List[int], List[int]]:
    """Traverse backwards through the table, finding the matches
    
    The two output lists will hold line indices, NOT line numbers
    I'll make sure to add one to them later
    """
    p1 = len(arr) - 1
    p2 = len(arr[0]) - 1

    o1: List[int] = []
    o2: List[int] = []

    while p1 > 0 and p2 > 0:
        if is_eq(sl1[p1], sl2[p2]):
            o1.append(p1)
            o2.append(p2)
            p1 -= 1
            p2 -= 1
        else:
            if arr[p1 - 1][p2] == arr[p1][p2]:
                p1 -= 1
            else:
                p2 -= 1

    if p1 == 0 and p2 == 0:
        if is_eq(sl1[p1], sl2[p2]):
            o1.append(0)
            o2.append(0)
    elif p1 == 0:
        while p2 > 0:
            if is_eq(sl1[p1], sl2[p2]):
                o1.append(p1)
                o2.append(p2)
                p2 -= 1
            else:
                p2 -= 1
    else:
        while p1 > 0:
            if is_eq(sl1[p1], sl2[p2]):
                o1.append(p1)
                o2.append(p2)
                p1 -= 1
            else:
                p1 -= 1

    o1.reverse()
    o2.reverse()

    return (o1, o2)


def print_stack_helper(match: bool, s1: int, e1: int, s2: int, e2: int,
                       f1: str, f2: str, max_len: int) -> None:
    """Actually format it nicely"""
    # Now we'll finally add 1 to go from a line index to a line number

    col_width = len(f1) + len(str(max_len))

    if s1 == -1:
        print("Match:   " if match else "Mismatch:", f1,
              "None".ljust(col_width), f2, f"<{s2 + 1} .. {e2 + 1}>")
    elif s2 == -1:
        print("Match:   " if match else "Mismatch:", f1,
              f"<{s1 + 1} .. {e1 + 1}>".ljust(col_width), f2, "None")
    else:
        print("Match:   " if match else "Mismatch:", f1,
              f"<{s1 + 1} .. {e1 + 1}>".ljust(col_width), f2,
              f"<{s2 + 1} .. {e2 + 1}>")


def print_stack(o1: List[int], o2: List[int], f1: str, f2: str, l1: int,
                l2: int) -> None:
    """Figure out what to print

    This was vastly more difficult than any other part of this lab.
    Sorry that it's so messy.
    """
    p = 0  # Pointer to both of the lists

    # Current start points.  Again, indices
    s1 = 0
    s2 = 0

    max_len = max(l1, l2)

    # 4 options to start
    if o1[p] == 0 and o2[p] == 0:
        pass
    elif o1[p] == 0:
        print_stack_helper(False, -1, -1, 0, o2[p] - 1, f1, f2, max_len)
    elif o2[p] == 0:
        print_stack_helper(False, 1, o1[p] - 1, -1, -1, f1, f2, max_len)
    else:
        print_stack_helper(False, 0, o1[p] - 1, 0, o2[p] - 1, f1, f2, max_len)

    s1 = o1[p]
    s2 = o2[p]

    while p < len(o1) - 1:  # len(o1) == len(o2)
        if o1[p + 1] == o1[p] + 1 and o2[p + 1] == o2[p] + 1:
            p += 1
        else:
            print_stack_helper(True, s1, o1[p], s2, o2[p], f1, f2, max_len)
            # We've reached the end of a matching block.
            if o1[p + 1] == o1[p] + 1:
                print_stack_helper(False, -1, -1, o2[p] + 1, o2[p + 1] - 1, f1,
                                   f2, max_len)
            elif o2[p + 1] == o2[p] + 1:
                print_stack_helper(False, o1[p] + 1, o1[p + 1] - 1, -1, -1, f1,
                                   f2, max_len)
            else:
                print_stack_helper(False, o1[p] + 1, o1[p + 1] - 1, o2[p] + 1,
                                   o2[p + 1] - 1, f1, f2, max_len)
            p += 1
            s1 = o1[p]
            s2 = o2[p]

    # Now we're on the last one
    print_stack_helper(True, s1, o1[p], s2, o2[p], f1, f2, max_len)

    # Edge cases on the end
    if o1[p] != l1 - 1 and o2[p] != l2 - 1:
        print_stack_helper(False, o1[p] + 1, l1 - 1, o2[p] + 1, l2 - 1, f1, f2,
                           max_len)
    elif o1[p] != l1 - 1:
        print_stack_helper(False, o1[p] + 1, l1 - 1, -1, -1, f1, f2, max_len)
    elif o2[p] != l2 - 1:
        print_stack_helper(False, -1, -1, o2[p] + 1, l2 - 1, f1, f2, max_len)


if __name__ == "__main__":
    # Get the file names
    if len(sys.argv) != 3:
        f1 = input("Enter the name of file 1: ")
        f2 = input("Enter the name of file 2: ")
    else:
        f1 = sys.argv[1]
        f2 = sys.argv[2]

    # Get all of the lines of the files, and calculate their hashes
    sl1: List[SHPair] = []
    with open(f1) as f:
        for line in f:
            sl1.append(SHPair(line, hash_fn(line)))

    sl2: List[SHPair] = []
    with open(f2) as f:
        for line in f:
            sl2.append(SHPair(line, hash_fn(line)))

    arr = fill_table(sl1, sl2)
    stack = traverse_table(sl1, sl2, arr)
    print_stack(*stack, f1, f2, len(sl1), len(sl2))

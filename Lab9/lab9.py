"""CMPE 365 Lab 9

2019-11-04

Troy Giorshev
20012707
15tag2

I certify that this submission contains my own work, except as noted.

==Assumptions==

None Needed.

==Other Notes==

python, mypy, yapf, pylint, yapf

"""
from typing import Callable, Dict


def f1(s: str) -> int:
    """Function 1
    This is generally regarded to be a poor function for this purpose, but 
    it was actually recommended in a famous text-book
    WHAT HOW WHY HOW
    I hope it was recommended as a bad example...
    <https://www.youtube.com/watch?v=ECQyFzzBHlo>
    OH I FOUND IT!
    It's in the first edition K&R!
    <http://www.cse.yorku.ca/~oz/hash.html>
    """

    ret = 0  # sum is a python builtin
    for c in s:
        ret += ord(c)
    return ret


def f2(s: str) -> int:
    """Function 2"""

    ret = 0
    for c in s:
        ret = 2 * ret + ord(c)
    return ret

def f3(s: str) -> int:
    """Function 3, possibly what python actually uses for dict."""
    ret = ord(s[0]) << 7
    for c in s[1:]:
        ret = ((1000003 * ret) ^ ord(c)) % (1<<32)
    return ret


def eval_fn(fn: Callable[[str], int], _f: str) -> float:
    """Evaluate the performance of a given function
    Ah I had to think about it for a second but it's easy to make this O(n)
    Python dictionaries are hash maps
    Hash maps search and insert in O(1)
    """
    num_comparisons = 0
    num_collisions = 0
    used: Dict[int, str] = dict()

    with open(_f) as f:
        for word in f:
            num_comparisons += 1
            val = fn(word)
            if val in used:
                num_collisions += 1
            else:
                used[val] = word

    return num_collisions / num_comparisons


def main() -> None:
    """Main"""
    print(f"F1 Collision Ratio: {eval_fn(f1, 'words1.txt'):0.2}")
    print(f"F2 Collision Ratio: {eval_fn(f2, 'words1.txt'):0.2}")
    # Wow that was a lot better
    print(f"F3 Collision Ratio: {eval_fn(f3, 'words1.txt'):0.2}")
    # 0 collisions!


main()

"""CMPE 365 Lab 4 + 5 / Assignment 2

2019-10-12 (3 Weeks: 11-02)

Troy Giorshev
20012707
15tag2

I certify that this submission contains my own work, except as noted.

==Assumptions==

None Needed.

==Other Notes==

pylint, YAPF, mypy

I'm going to avoid using lists of integers, because there's no good way to
differentiate between lists of integers and lists of sets.
So lists will always be lists of sets.  (Once possible)

Recall that we're just trying to find **a** solution, we don't care about the
number of coins (or whatever)

"""

import math
import random
import matplotlib.pyplot as plt
import os

class Set:  # pylint: disable=too-few-public-methods
    """Set class"""
    elements: list
    sum: int

    def __init__(self, L: list):
        """Inits Set, automatically calculating sum"""
        self.elements = L
        self.sum = sum(L)  # This is 0 if len(L)=0


# Is there a name for a "constant" object?
EMPTY_SET = Set([])
count = 0


def bfi_subset_sum_alg(full: Set, k: int) -> Set:
    """Solve the subset sum problem with Brute Force and Ignorance

    I've left this here just for reference, it isn't used in the
    solution to the assignment.

    Arguments:
        full:  Set of integers
        k:  The goal that the chosen subset should sum to
    Returns:
        The best subset, or the empty set if none is found
    """
    global count

    subsets = []
    subsets.append(EMPTY_SET)

    for _, elem in enumerate(full.elements):
        new_subsets = []
        for old_u in subsets:
            new_u = Set(old_u.elements + [elem])
            # Sum is calculated automatically
            count += 2 * len(new_u.elements) + 1
            # It takes len(new_u.elements) operations to make the set
            # Then another len(new_u.elements) to calculate the sum
            # Then another 1 to do the check immediately below
            if new_u.sum == k:
                return new_u
            new_subsets.append(old_u)
            new_subsets.append(new_u)
        subsets = new_subsets

    return EMPTY_SET


def bfi_subset_sum(full: list, k: int) -> None:
    """Wrapper for the BFI algorithm
    
    Arguments:
        S:  list of integers
        k:  The goal that the chosen subset should sum to
    """
    options = Set(full)
    result = bfi_subset_sum_alg(options, k)
    if result.sum == 0:
        print("No subset found")
    else:
        print(f"BFI Solution found: {result.elements}")


def get_subsets(full: Set, k: int) -> list:
    """Return a list of all of the subsets of the input set

    This ends early if any of the subsets work.

    Arguments:
        full:  Set of integers AT LEAST ONE ELEMENT
        k:  The goal that the chosen subset should sum to
    Returns:
        List of all subsets, or a singleton list if a working subset is found
    """
    global count

    subsets = []
    subsets.append(EMPTY_SET)

    for _, elem in enumerate(full.elements):
        new_subsets = []
        for old_u in subsets:
            new_u = Set(old_u.elements + [elem])
            # Sum is calculated automatically
            count += 2 * len(new_u.elements) + 1
            # It takes len(new_u.elements) operations to make the set
            # Then another len(new_u.elements) to calculate the sum
            # Then another 1 to do the check immediately below
            if new_u.sum == k:
                return [new_u]
            new_subsets.append(old_u)
            new_subsets.append(new_u)
        subsets = new_subsets

    return subsets


def hs_subset_sum_alg(full: Set, k: int) -> Set:
    """Solve the subset sum problem with The Horowitz-Sahni Algorithm

    Arguments:
        full:   Set of integers AT LEAST TWO ELEMENTS
        k:      The goal that the chosen subset should sum to
    Returns:
        The best subset, or the empty set if none is found
    """
    global count

    full_left = Set(full.elements[:len(full.elements) // 2])
    count += 2 * len(full_left.elements)
    full_right = Set(full.elements[len(full.elements) // 2:])
    count += 2 * len(full_right.elements)

    subsets_left = get_subsets(full_left, k)
    count += 1
    if len(subsets_left) == 1:
        # I don't have to check k again, if there's only one element
        # then that must be the one. (From how get_subsets() works)
        return subsets_left[0]
    subsets_right = get_subsets(full_right, k)
    count += 1
    if len(subsets_right) == 1:
        return subsets_right[0]
    # If k was in either we would have found it by now
    # On to pair sum!  I'm gonna just write it in here...
    subsets_left.sort(key=lambda x: x.sum)
    count += 3 * len(subsets_left) * int(math.log2(len(subsets_left)))
    subsets_right.sort(key=lambda x: x.sum)
    count += 3 * len(subsets_right) * int(math.log2(len(subsets_right)))
    p1 = 0
    p2 = len(subsets_right) - 1
    while (p1 < len(subsets_left) and p2 >= 0):
        tmp = subsets_left[p1].sum + subsets_right[p2].sum
        count += 3  # 2 above, then 1 for the if
        if tmp == k:
            ret = Set(subsets_left[p1].elements + subsets_right[p2].elements)
            count += 2 * len(ret.elements)
            return ret
        count += 1
        if tmp < k:
            p1 += 1
        else:
            p2 -= 1
        count += 2 # For the two checks in the while condition
    return EMPTY_SET

def hs_subset_sum(S: list, k: int) -> None:
    """Wrapper for my Horowitz-Sahni algorithm
    
    Arguments:
        S:  list of integers
        k:  The goal that the chosen subset should sum to
    """
    if k == 0:
        print("Solution found: do nothing!")
        return
    if len(S) == 0:  # pylint: disable=len-as-condition
        print("No solution found, no options given")
        return
    if len(S) == 1:
        if S[0] == k:
            print(f"Solution Found: {S}")
            return
        print("No solution found.")
        return
    # Okay now that that's out of the way...
    options = Set(S)
    best = hs_subset_sum_alg(options, k)
    if best.sum == 0:
        print("No solution found")
    else:
        print(f"HS Solution Found:  {best.elements}")


def test() -> None:
    """Run tests for each algorithm"""
    global count

    # Normal
    print("Normal, summing to 28")
    S = [3, 5, 3, 9, 18, 4, 5, 6]
    total = 28
    count = 0
    hs_subset_sum(S, total)
    print(count)
    count = 0
    bfi_subset_sum(S, total)
    print(count)
    print()

    # Empty
    print("Empty list")
    S = []
    total = 5
    count = 0
    hs_subset_sum(S, total)
    print(count)
    count = 0
    bfi_subset_sum(S, total)
    print(count)
    print()

    # No solution
    print("Normal, no solution")
    S = [3, 5, 3, 9, 18, 4, 5, 6]
    total = 52
    count = 0
    hs_subset_sum(S, total)
    print(count)
    count = 0
    bfi_subset_sum(S, total)
    print(count)
    print()

    # One element solution
    print("One element solution")
    S = [5]
    total = 5
    count = 0
    hs_subset_sum(S, total)
    print(count)
    count = 0
    bfi_subset_sum(S, total)
    print(count)
    print()

    # Sum everything
    print("Sum everything")
    S = [1, 2, 3, 4, 5]
    total = 15
    count = 0
    hs_subset_sum(S, total)
    print(count)
    count = 0
    bfi_subset_sum(S, total)
    print(count)
    print()

    # Solution where you need to combine the two
    print("Subset requiring combination")
    S = [1, 1, 10, 10]
    total = 21
    count = 0
    hs_subset_sum(S, total)
    print(count)
    count = 0
    bfi_subset_sum(S, total)
    print(count)
    print()

    # Solution where target is in the set
    print("Target in set, and there's an option that makes it")
    S = [40, 60, 100]
    total = 100
    count = 0
    hs_subset_sum(S, total)
    print(count)
    count = 0
    bfi_subset_sum(S, total)
    print(count)
    print()

def experiment() -> None:
    bfi_x = []
    bfi_y = []
    hs_x = []
    hs_y = []

    for n in range(4,15):       # Set size
        hs_n = 0
        bfi_n = 0
        for _ in range(1,20):   # Number of tests
            hs = 0
            bfi = 0
            S = [random.randint(1,100) for i in range(n)]
            targets = [random.randint(30,200) for i in range(10)]
            for total in targets:
                count = 0
                hs_subset_sum(S, total)
                hs += count
                count = 0
                bfi_subset_sum(S, total)
                bfi += count
            hs_n += hs / 10
            bfi_n += bfi / 10
        hs_n  = hs_n / 20
        bfi_n = bfi_n / 20
        bfi_x.append(n)
        bfi_y.append(bfi_n)
        hs_x.append(n)
        hs_y.append(hs_n)

    print(bfi_x)
    print(bfi_y)

    plt.scatter(bfi_x, bfi_y)
    plt.title("BFI scatter plot")
    plt.xlabel("n")
    plt.savefig("This.png")

    plt.scatter(hs_x, hs_y)
    plt.title("HS scatter plot")
    plt.xlabel("n")
    plt.ylabel("# operations")
    #plt.show()


def main() -> None:
    """Main"""
    test()
    experiment()


if __name__ == "__main__":
    main()

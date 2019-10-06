"""CMPE 365 Lab 3

Troy Giorshev

Playing around with binary and trinary searches

My solution is off from Dawes's by 2, just because we count differently.
My "1000" uses an array of size "500", so we're checking about 1000 numbers
His "1000" uses an array of size "1000", so he's checking about 2000 numbers

Learned:
Format string inside f string     🠓
print(f"{num}: Trin avg {sum / num:.2f}")
"""


def bin_search(A: list, x: int) -> (int, int):
    """Binary search sorted ist A for x
    
    Args:
        A:  Sorted list of integers
        x:  Integer to find
    Returns:
        The index of x, or -1 if not found
        The number of comparisons
    """
    first = 0
    last = len(A) - 1

    comparisons = 0

    while first <= last:
        mid = (first + last) // 2
        comparisons += 2
        if A[mid] == x:
            comparisons -= 1
            return (mid, comparisons)
        elif A[mid] > x:
            last = mid - 1
        else:
            first = mid + 1
    return (-1, comparisons)


def trin_search(A: list, x: int) -> int:
    """Return the index of x in sorted list A, or -1 if not found"""
    first = 0
    last = len(A) - 1

    comparisons = 0

    while first <= last:
        t1 = first + (last - first) // 3
        comparisons += 2
        if A[t1] == x:
            comparisons -= 1
            return (t1, comparisons)
        elif A[t1] > x:
            last = t1 - 1
        else:
            first = t1 + 1
            if first > last:
                return (-1, comparisons)
            mid = (first + last) // 2
            comparisons += 2
            if A[mid] == x:
                comparisons -= 1
                return (mid, comparisons)
            elif A[mid] > x:
                last = mid - 1
            else:
                first = mid + 1
    return (-1, comparisons)


def test(num: int) -> None:
    """Tests binary and trinary searches.  Odd n please"""
    A = [x * 2 for x in range(1, (num + 1) // 2)]

    sum = 0
    for i in range(1, num + 1):
        (index, comparisons) = bin_search(A, i)
        sum += comparisons
        #print(f"{i}: {index} \t {comparisons} comps")

    print(f"{num}: Bin avg {sum / num:.2f}")

    sum = 0
    for i in range(1, num + 1):
        (index, comparisons) = trin_search(A, i)
        sum += comparisons
        #print(f"{i}: {index} \t {comparisons} comps")

    print(f"{num}: Trin avg {sum / num:.2f}")
    print()


if __name__ == "__main__":
    test(1001)
    test(2001)
    test(4001)
    test(8001)
    test(16001)

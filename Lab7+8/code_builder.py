"""CMPE 365 Lab 7 + 8 / Assignment 3
Code-Building Module

Troy Giorshev
20012707
15tag2

I certify that this submission contains my own work, except as noted.

==Assumptions==

None Needed.

==Other Notes==`

python, mypy, yapf, pylint, yapf

"""

# From others
## For type hinting
from typing import List
## For actually useful stuff
from pathlib import Path
from heapq import heapify, heappush, heappop
# Now my custom Node
from node import Node


def count_chars(freq: dict, fl: Path) -> None:
    """Read file and increment frequency dictionary values"""
    with open(fl) as f:
        text = f.read()  # Meh I have enough ram
        for c in text:
            try:
                freq[str(ord(c))] += 1
            except:
                continue


def print_dict(freq: dict) -> None:
    """Print out the dictionary nicely"""
    for k, v in freq.items():
        if len(k) == 2:
            print(f"{k}:  {v}")
        else:
            print(f"{k}: {v}")


def find_frequencies(folder: Path) -> dict:
    """Build the frequency dictionary from files in a folders"""

    # Initialize the frequencies dictionary with all zeroes
    frequencies = {}

    frequencies["10"] = 0
    for i in range(32, 127):
        frequencies[str(i)] = 0

    files = folder.glob("*")

    for file in files:
        count_chars(frequencies, file)  # This modifies `frequencies`

    #print_dict(frequencies)

    return frequencies


def traverse(node: Node, label: List, labels: dict) -> None:
    """Traverse the Huffman binary tree, labeling codewords"""
    if node.left_child is None and node.right_child is None:
        labels[node.name] = ''.join(label)
        return
    if node.left_child is not None:
        tmp = list(label)
        tmp.append("0")
        traverse(node.left_child, tmp, labels)
    if node.right_child is not None:
        tmp = list(label)
        tmp.append("1")
        traverse(node.right_child, tmp, labels)


def build(folder: Path, name: str) -> None:
    """Build the Code from files in a folder"""
    # Find all of the frequencies
    frequencies = find_frequencies(folder)

    # We're going to be repeatedly popping the "smallest" one
    # So let's use a heap
    # Heap of node objects!
    heap: List[Node] = []
    for k, v in frequencies.items():
        heap.append(Node(k, v))

    heapify(heap)    # Linear time

    while len(heap) > 1:
        # Get the two smallest objects
        one = heappop(heap)
        two = heappop(heap)

        # Make a new node and push that to the heap
        new = Node(one.name + "," + two.name, one.freq + two.freq)
        new.left_child = one
        one.parent = new
        new.right_child = two
        two.parent = new
        heappush(heap, new)

    # Now traverse down the tree, assigning numbers
    # and extract them to a dictionary
    labels = {}

    labels["10"] = ""
    for i in range(32, 127):
        labels[str(i)] = ""

    traverse(heap[0], [], labels)

    print_dict(labels)

    # Output to a file
    with open(name, "w") as f:
        for k, v in labels.items():
            f.write(f"{k} {v}\n")


if __name__ == "__main__":
    build(Path("TestCC"), "code.txt")

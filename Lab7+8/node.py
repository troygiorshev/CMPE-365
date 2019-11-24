"""CMPE 365 Lab 7 + 8 / Assignment 3
Node class

Troy Giorshev
20012707
15tag2

I certify that this submission contains my own work, except as noted.

==Assumptions==

None Needed.

==Other Notes==`

python, mypy, yapf, pylint, yapf

"""

from typing import Optional


class Node:
    """A node of the Huffman binary tree"""
    def __init__(self, name: Optional[str], freq: Optional[int]) -> None:
        """Initialize Node"""
        self.name: Optional[str] = name
        self.freq: Optional[int] = freq
        self.parent: Optional[Node] = None
        self.left_child: Optional[Node] = None
        self.right_child: Optional[Node] = None

    # Implement the rich comparison methods
    # I can't type hint `other: Node` inside these, weird
    def __lt__(self, other) -> bool:
        return self.freq < other.freq

    def __gt__(self, other) -> bool:
        return self.freq > other.freq

    def __le__(self, other) -> bool:
        return self.freq <= other.freq

    def __ge__(self, other) -> bool:
        return self.freq >= other.freq

    def __eq__(self, other) -> bool:
        return self.freq == other.freq

    # Note: Recall `is` to check if two objects are actually the same thing

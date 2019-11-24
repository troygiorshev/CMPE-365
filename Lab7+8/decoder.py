"""CMPE 365 Lab 7 + 8 / Assignment 3
Decoder Module

Troy Giorshev
20012707
15tag2

I certify that this submission contains my own work, except as noted.

==Assumptions==

None Needed.

==Other Notes==`

python, mypy, yapf, pylint, yapf

"""

from pathlib import Path
from node import Node


class Decoder:
    """Decoder Object"""
    def __init__(self, codebooklocation: Path) -> None:
        """Initialize the Decoder Object"""
        self.tree = Node("root", None)
        with open(codebooklocation) as f:
            for line in f:
                name, label = line.split()
                p = self.tree
                for i, c in enumerate(label):
                    if c == "0":
                        if p.left_child:
                            p = p.left_child
                        else:
                            tmp = Node(None, None)
                            p.left_child = tmp
                            p = p.left_child
                    else:
                        if p.right_child:
                            p = p.right_child
                        else:
                            tmp = Node(None, None)
                            p.right_child = tmp
                            p = p.right_child
                    if i == len(label) - 1:
                        p.name = name


    def decode_file(self, file: Path) -> None:
        """Decode a single file"""
        p = self.tree
        with open(file) as f:
            out = []
            text = f.read()
            for c in text:
                if c == "0":
                    p = p.left_child
                else:
                    p = p.right_child
                if p.name:
                    out.append(chr(int(p.name)))
                    p = self.tree

            print(Path(file).with_suffix(".dec"))

            with open(Path(file).with_suffix(".dec"), "w") as o:
                o.write(''.join(out))


    def decode(self, folder: Path) -> None:
        """Decode all files in a folder"""
        files = folder.glob("*.enc")

        for file in files:
            self.decode_file(file)


if __name__ == "__main__":
    in_file = input("Enter the path to the file to decode: ")
    code = input("Enter the path to the code-string dictionary: ")

    de = Decoder(Path(code))
    de.decode_file(Path(in_file))

"""CMPE 365 Lab 7 + 8 / Assignment 3
Encoder Module

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
from typing import Dict


class Encoder:
    """Encoder object"""
    def __init__(self, codebooklocation: Path) -> None:
        """Initialize the encoder object, given a codebook"""
        self.codebook: Dict[str, str] = dict()
        with open(codebooklocation) as c:
            for line in c:
                k, v = line.split()
                self.codebook[k] = v

    def encode_file(self, file: Path) -> None:
        """Encode one text file"""
        with open(file) as f:
            out = []
            text = f.read()
            for c in text:
                try:
                    out.append(self.codebook[str(ord(c))])
                except:
                    continue

            print(Path(file).with_suffix(".enc"))

            with open(Path(file).with_suffix(".enc"), "w") as o:
                o.write(''.join(out))

    def encode(self, folder: Path) -> None:
        """Encode all of the text files in a folder"""
        files = folder.glob("*.txt")

        for file in files:
            self.encode_file(file)

if __name__ == "__main__":
    in_file = input("Enter the path to the file to encode: ")
    code = input("Enter the path to the code-string dictionary: ")

    en = Encoder(Path(code))
    en.encode_file(Path(in_file))

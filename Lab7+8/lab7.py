"""CMPE 365 Lab 7 + 8 / Assignment 3

2019-11-02 (3 Weeks: 11-23)

Troy Giorshev
20012707
15tag2

I certify that this submission contains my own work, except as noted.

==Assumptions==

None Needed.

==Other Notes==

python, mypy, yapf, pylint, yapf

"""

# Others
from pathlib import Path
from typing import Dict
# Me
from code_builder import build
#from code_builder import print_dict
from encoder import Encoder
from decoder import Decoder


def test1():
    """Test that I'm using ordinals correctly"""
    print(f"10: \"{chr(10)}\"")
    for i in range(32, 127):
        print(f"{i}: \"{chr(i)}\"")


def part1():
    """Part 1"""
    build(Path("TestCC"), "code.txt")
    en = Encoder(Path("code.txt"))
    en.encode(Path("TestData"))
    de = Decoder(Path("code.txt"))
    de.decode(Path("TestData"))
    original = open("TestData/File2.txt").read()
    decoded = open("TestData/File2.dec").read()

    if original == decoded:
        print("Same!")


def part2():
    """Part 2"""
    build(Path("CC1"), "code1.txt")
    build(Path("CC2"), "code2.txt")
    build(Path("CC3"), "code3.txt")
    en1 = Encoder(Path("code1.txt"))
    en2 = Encoder(Path("code2.txt"))
    en3 = Encoder(Path("code3.txt"))
    de1 = Decoder(Path("code1.txt"))
    de2 = Decoder(Path("code2.txt"))
    de3 = Decoder(Path("code3.txt"))

    data = Path("Data")
    # sizes: [original, cc1, cc2, cc3]
    dataDict: Dict(str, [int, int, int, int]) = {}

    files = data.glob("*.txt")

    for file in files:
        dataDict[file] = [file.stat().st_size, 0, 0, 0]

    for i, (en, de) in enumerate([(en1, de1), (en2, de2), (en3, de3)]):
        en.encode(data)
        de.decode(data)

        # Verify that they are right
        # This takes a minute so I've commented it out
        """
        files = data.glob("*.txt")
        for file in files:
            original = open(file).read()
            decoded = open(file.with_suffix(".dec")).read()
            original_clean = []
            valid = [10] + [x for x in range(32, 127)]
            for c in original:
                if ord(c) in valid:
                    original_clean.append(c)
            original_clean = ''.join(original_clean)
            if original_clean != decoded:
                print(f"{file.name} failed")
        """

        files = data.glob("*.txt")
        for file in files:
            encoded = file.with_suffix(".enc")
            dataDict[file][i + 1] = encoded.stat().st_size // 8

    for (k, v) in dataDict.items():
        print(f"{k.name}:\t{v}")


def main():
    """Main"""
    part1()
    #part2()


if __name__ == "__main__":
    main()

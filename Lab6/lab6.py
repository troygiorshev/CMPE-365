"""CMPE 365 Lab 6

Troy Giorshev

Workflow: python, mypy, yapf, pylint, yapf

"""

import random


def generate_boxes(num: int) -> list:
    """Randomly generate the chocolate boxes"""
    return [random.randint(1, 1000000) for i in range(num)]


def w_w(boxes: list, k: int) -> int:
    """Odds Algorihtm

    Arguments:
        boxes:  list of integers, representing the number of chocolates
                    in the particular box
        k:      the number of boxes to be skipped
    Returns:
        The index of the box to choose
    """
    best = 0
    for i in range(k):
        if boxes[i] > best:
            best = boxes[i]
    for i in range(k, len(boxes)):
        if boxes[i] > best:
            return i
    return len(boxes) - 1


def part1():
    """Test that things are working correctly"""
    boxes = generate_boxes(100)
    choose = w_w(boxes, int(len(boxes) * 0.37))
    print(f"Pick box at index {choose}, with {boxes[choose]} chocolates.")
    if boxes[choose] == max(boxes):
        print("The right box was chosen!")
    else:
        print(f"Could have done better.  Best was {max(boxes)}")


def part2() -> None:
    """Perform the experiment"""
    for num in [10000, 20000, 40000, 80000, 160000]:
        count_wins = dict.fromkeys(range(35, 40), 0)
        for _ in range(500):
            boxes = generate_boxes(num)
            for k_percent in range(35, 40):
                chosen = w_w(boxes, int((k_percent / 100) * len(boxes)))
                if boxes[chosen] == max(boxes):
                    count_wins[k_percent] += 1
        print()
        print(num)
        for k_percent in range(35, 40):
            print(k_percent, count_wins[k_percent] / 500)


def main() -> None:
    """Main"""
    part1()
    part2()


if __name__ == "__main__":
    main()

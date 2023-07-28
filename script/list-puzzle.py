# -*- coding: utf-8 -*- #
import json


def cut_data(pid, data):
    puz = ""
    if data["name"] != "":
        puz += data["name"]
        if data["name_e"] != "":
            puz += " (" + data["name_e"] + ")"
    else:
        puz += data["name_e"]

    puz += f"\thttps://puzsq.logicpuzzle.app/?kind={pid}"
    return puz


def main():
    kind = {}

    with open("data/kind.json", encoding='utf8') as fi:
        kind = json.load(fi)

    puzzles = []
    for pid, data in kind.items():
        puzzles.append(cut_data(pid, data))
    list.sort(puzzles)

    with open("data/puzzle_list.txt", "w") as fo:
        for p in puzzles:
            fo.write(p)
            fo.write('\n')


if __name__ == '__main__':
    main()

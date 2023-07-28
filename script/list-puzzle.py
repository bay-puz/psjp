# -*- coding: utf-8 -*- #
import json


def cut_data(pid, data):
    name = ""
    if data["name"] != "":
        name += data["name"]
        if data["name_e"] != "" and data["name"] != data["name_e"]:
            name += " (" + data["name_e"] + ")"
    else:
        name += data["name_e"]

    url = f"https://puzsq.logicpuzzle.app/?kind={pid}"

    return f"1. {name} [🔗]({url})"


def main():
    kind = {}

    with open("data/kind.json", encoding='utf8') as fi:
        kind = json.load(fi)

    puzzles = []
    for pid, data in kind.items():
        puzzles.append(cut_data(pid, data))
    list.sort(puzzles)

    with open("data/puzzle_list.md", "w") as fo:
        fo.write("# ぱずすくのパズルのリスト\n")
        for p in puzzles:
            fo.write(p)
            fo.write('\n')


if __name__ == '__main__':
    main()

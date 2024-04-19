# -*- coding: utf-8 -*- #
import json


def markdown(p_dict: dict):
    pid = p_dict["pid"]
    name = p_dict["name"]
    count = p_dict["count"]
    url = f"https://puzsq.logicpuzzle.app/?kind={pid}"
    return f"1. [{name}]({url}) ({count})"


def main():
    kind = {}
    with open("data/kind.json", encoding='utf8') as fk:
        kind = json.load(fk)

    puzzle = {}
    with open("data/puzzle.json", encoding='utf8') as fp:
        puzzle = json.load(fp)

    puzzles_dict = {}
    for pid in kind:
        p_dict = {"pid": pid, "name": "", "count": 0}
        name_ja = kind[pid]["name"].strip()
        name_en = kind[pid]["name_e"].strip()
        if len(name_ja) > 0:
            p_dict["name"] += name_ja
            if len(name_en) > 0 and name_en != name_ja:
                p_dict["name"] += " (" + name_en + ")"
        else:
            p_dict["name"] += name_en
        if pid in puzzle:
            p_dict["count"] = puzzle[pid]["problem_n"]
        puzzles_dict[pid] = p_dict
    puzzles = sorted(puzzles_dict.values(), key=lambda x: x["name"])

    with open("data/puzzle_list.md", "w") as fo:
        fo.write("# ぱずすくのパズルのリスト")
        fo.write('\n\n')
        for puzzle in puzzles:
            fo.write(markdown(puzzle))
            fo.write('\n')


if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*- #
import json
import argparse


def cut_data(data: list):
    author_dict = {}
    puzzle_dict = {}
    for d in data:
        if d["author_name"] not in author_dict:
            author = {"id": d["author_id"], "liked": 0, "problem": 0, "puzzle": []}
            author_dict[d["author_name"]] = author
        author_dict[d["author_name"]]["liked"] += d["liked"]
        author_dict[d["author_name"]]["problem"] += 1
        if d["puzzle_name"] not in author_dict[d["author_name"]]["puzzle"]:
            author_dict[d["author_name"]]["puzzle"].append(d["puzzle_name"])

        if d["puzzle_name"] not in puzzle_dict:
            puzzle = {"id": d["puzzle_id"], "liked": 0, "problem": 0, "author": []}
            puzzle_dict[d["puzzle_name"]] = puzzle
        puzzle_dict[d["puzzle_name"]]["liked"] += d["liked"]
        puzzle_dict[d["puzzle_name"]]["problem"] += 1
        if d["author_name"] not in puzzle_dict[d["puzzle_name"]]["author"]:
            puzzle_dict[d["puzzle_name"]]["author"].append(d["author_name"])

    return author_dict, puzzle_dict


def load(file: str):
    with open(file, encoding='utf8') as f:
        data_json = f.read()
        return json.loads(data_json)


def write(data: dict, file: str):
    with open(file, 'w', encoding="utf8") as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description='PSJPの問題毎のデータを作者毎・パズル毎に変換する')
    parser.add_argument("--input", type=str, default="data/data.json", help="問題別データの書かれたファイル")
    parser.add_argument("--author", type=str, default="data/author.json", help="作者別データの出力先")
    parser.add_argument("--puzzle", type=str, default="data/puzzle.json", help="パズル別データの出力先")
    args = parser.parse_args()

    data = load(args.input)
    authors, puzzles = cut_data(data)

    write(authors, args.authors)
    write(puzzles, args.puzzles)

    return

if __name__ == '__main__':
    main()
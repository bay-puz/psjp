# -*- coding: utf-8 -*- #
import json
import argparse


def cut_data(data: list, is_author: bool):
    cut_dict = {}

    all_name = "全作者" if is_author else "全パズル"
    category = "author" if is_author else "puzzle"
    another = "puzzle" if is_author else "author"

    category_id = category + "_id"
    category_name = category + "_name"
    another_name = another + "_name"

    all = {"name": all_name, "id": 0, "liked": 0, "problem": 0, "difficulty": [0 for _ in range(6)], "variant": 0, another: {}}
    cut_dict[all_name] = all

    for d in data:
        d_name = d[category_name]
        d_another_name = d[another_name]

        if d_name not in cut_dict:
            data_format = {"name": d_name, "id": d[category_id], "liked": 0, "problem": 0, "difficulty": [0 for _ in range(6)], "variant": 0, another: {}}
            cut_dict[d_name] = data_format
        for name in [d_name, all_name]:
            cut_dict[name]["liked"] += d["liked"]
            cut_dict[name]["problem"] += 1
            cut_dict[name]["difficulty"][d["difficulty"]] += 1
            if d["variant"] == 1:
                cut_dict[name]["variant"] += 1

        for name in [d_name, all_name]:
            if d_another_name not in cut_dict[name][another]:
                another_format = {"name": d_another_name, "liked": 0, "problem": 0, "difficulty": [0 for _ in range(6)], "variant": 0}
                cut_dict[name][another][d_another_name] = another_format
            cut_dict[name][another][d_another_name]["liked"] += d["liked"]
            cut_dict[name][another][d_another_name]["problem"] += 1
            cut_dict[name][another][d_another_name]["difficulty"][d["difficulty"]] += 1
            if d["variant"] == 1:
                cut_dict[name][another][d_another_name]["variant"] += 1

    for key in cut_dict.keys():
        cut_dict[key]["count"] = len(cut_dict[key][another])

    return cut_dict


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
    authors = cut_data(data, is_author=True)
    puzzles = cut_data(data, is_author=False)

    write(authors, args.author)
    write(puzzles, args.puzzle)

    return

if __name__ == '__main__':
    main()
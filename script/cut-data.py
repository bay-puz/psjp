# -*- coding: utf-8 -*- #
import json
import argparse


def set_data_dict(d_id: int, another: str = "") -> dict:
    d = {"id": d_id, "problem_n": 0, "favorite_n": 0, "answered_n": 0, "variant_n": 0}
    d["difficulty"] = [{"number": n + 1, "problem_n": 0, "favorite_n": 0, "answered_n": 0, "variant_n": 0} for n in range(5)]
    if len(another) > 0:
        d[another] = {}
    return d


def cut_data(data: list, is_author: bool):
    cut_dict = {}

    another = "kind" if is_author else "author"
    data_category_id = "user" if is_author else "kind"
    data_another_id = "kind" if is_author else "user"

    all_id = 0
    cut_dict[all_id] = set_data_dict(all_id, another)

    for d in data.values():
        d_id = d[data_category_id]
        d_another_id = d[data_another_id]
        d_difficulty = d["difficulty"] - 1

        if d_id not in cut_dict:
            cut_dict[d_id] = set_data_dict(d_id, another)
        for c_id in [d_id, all_id]:
            for key in ["favorite_n", "answered_n"]:
                cut_dict[c_id][key] += d[key]
                cut_dict[c_id]["difficulty"][d_difficulty][key] += d[key]
            cut_dict[c_id]["problem_n"] += 1
            cut_dict[c_id]["difficulty"][d_difficulty]["problem_n"] += 1
            if d["variation"] == 1:
                cut_dict[c_id]["variant_n"] += 1
                cut_dict[c_id]["difficulty"][d_difficulty]["variant_n"] += 1

        for c_id in [d_id, all_id]:
            if d_another_id not in cut_dict[c_id][another]:
                cut_dict[c_id][another][d_another_id] = set_data_dict(d_another_id)
            for key in ["favorite_n", "answered_n"]:
                cut_dict[c_id][another][d_another_id][key] += d[key]
                cut_dict[c_id][another][d_another_id]["difficulty"][d_difficulty][key] += d[key]
            cut_dict[c_id][another][d_another_id]["problem_n"] += 1
            cut_dict[c_id][another][d_another_id]["difficulty"][d_difficulty]["problem_n"] += 1
            if d["variation"] == 1:
                cut_dict[c_id][another][d_another_id]["variant_n"] += 1
                cut_dict[c_id][another][d_another_id]["difficulty"][d_difficulty]["variant_n"] += 1

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
    write(authors, args.author)

    puzzles = cut_data(data, is_author=False)
    write(puzzles, args.puzzle)


if __name__ == '__main__':
    main()

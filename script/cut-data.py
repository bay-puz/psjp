# -*- coding: utf-8 -*- #
import json
import argparse


def cut_data(data: list, is_author: bool, category_data: dict, another_data: dict):
    cut_dict = {}

    another = "kind" if is_author else "author"
    data_category_id = "user" if is_author else "kind"
    data_another_id = "kind" if is_author else "user"

    all_id = 0
    cut_dict[all_id] = {"id": all_id, "favorite_n": 0, "answered_n": 0, "problem_n": 0, "difficulty": [{"problem_n": 0, "favorite_n": 0, "answered_n": 0, "variant_n": 0} for _ in range(6)], "variant_n": 0, another: {}}

    for d in data.values():
        d_id = d[data_category_id]
        d_another_id = d[data_another_id]

        if d_id not in cut_dict:
            name = category_data[str(d_id)]["name"]
            data_format = {"id": d_id, "favorite_n": 0, "answered_n": 0, "problem_n": 0, "difficulty": [{"problem_n": 0, "favorite_n": 0, "answered_n": 0, "variant_n": 0} for _ in range(6)], "variant_n": 0, another: {}}
            cut_dict[d_id] = data_format
        for c_id in [d_id, all_id]:
            for key in ["favorite_n", "answered_n"]:
                cut_dict[c_id][key] += d[key]
                cut_dict[c_id]["difficulty"][d["difficulty"]][key] += d[key]
            cut_dict[c_id]["problem_n"] += 1
            cut_dict[c_id]["difficulty"][d["difficulty"]]["problem_n"] += 1
            if d["variation"] == 1:
                cut_dict[c_id]["variant_n"] += 1
                cut_dict[c_id]["difficulty"][d["difficulty"]]["variant_n"] += 1

        for c_id in [d_id, all_id]:
            if d_another_id not in cut_dict[c_id][another]:
                name = another_data[str(d_another_id)]["name"]
                another_format = {"id": d_another_id, "name": name, "favorite_n": 0, "answered_n": 0, "problem_n": 0, "difficulty": [{"problem_n": 0, "favorite_n": 0, "answered_n": 0, "variant_n": 0} for _ in range(6)], "variant_n": 0}
                cut_dict[c_id][another][d_another_id] = another_format
            for key in ["favorite_n", "answered_n"]:
                cut_dict[c_id][another][d_another_id][key] += d[key]
                cut_dict[c_id][another][d_another_id]["difficulty"][d["difficulty"]][key] += d[key]
            cut_dict[c_id][another][d_another_id]["problem_n"] += 1
            cut_dict[c_id][another][d_another_id]["difficulty"][d["difficulty"]]["problem_n"] += 1
            if d["variation"] == 1:
                cut_dict[c_id][another][d_another_id]["variant_n"] += 1
                cut_dict[c_id][another][d_another_id]["difficulty"][d["difficulty"]]["variant_n"] += 1

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
    parser.add_argument("--user", type=str, default="data/user.json", help="ユーザーデータの書かれたファイル")
    parser.add_argument("--kind", type=str, default="data/kind.json", help="パズルデータの書かれたファイル")
    parser.add_argument("--author", type=str, default="data/author.json", help="作者別データの出力先")
    parser.add_argument("--puzzle", type=str, default="data/puzzle.json", help="パズル別データの出力先")
    args = parser.parse_args()

    data = load(args.input)
    user_data = load(args.user)
    kind_data = load(args.kind)

    authors = cut_data(data, is_author=True, category_data=user_data, another_data=kind_data)
    write(authors, args.author)

    puzzles = cut_data(data, is_author=False, another_data=user_data, category_data=kind_data)
    write(puzzles, args.puzzle)


if __name__ == '__main__':
    main()

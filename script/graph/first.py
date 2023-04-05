# -*- coding: utf-8 -*- #
import json
from datetime import datetime
from matplotlib import pyplot


def load(file: str):
    with open(file, encoding='utf8') as f:
        data_json = f.read()
        return json.loads(data_json)


def get_first_categories(data: dict, is_author: bool, name_dict: dict):
    search = "kind" if is_author else "user"
    category = "user" if is_author else "kind"

    first_problem = {}
    for d in data.values():
        category_id = d[search]
        time = datetime.fromisoformat(d["registered"])
        if category_id in first_problem:
            if first_problem[category_id]["time"] > time:
                first_problem[category_id]["time"] = time
                first_problem[category_id]["id"] = d[category]
        else:
            first_problem[category_id] = {"time": time, "id": d[category]}

    counts_dict = {}
    for d in first_problem.values():
        id_str = str(d["id"])
        if id_str in counts_dict:
            counts_dict[id_str] += 1
        else:
            counts_dict[id_str] = 1

    sorted_dict = sorted(counts_dict.items(), key=lambda x: x[1])
    names = [name_dict[id_str]["name"] for id_str, _ in sorted_dict]
    counts = [count for _, count in sorted_dict]

    # 同名アカウントがあるときは id を付けて区別する
    if category == 'user':
        duplicated_names = []
        for name in names:
            if name in duplicated_names:
                continue
            if names.count(name) > 1:
                duplicated_names.append(name)
        for name_iter, name in enumerate(names):
            if name in duplicated_names:
                id_str, _ = sorted_dict[name_iter]
                name += ' (' + id_str + ')'
                names[name_iter] = name

    return names, counts


def plot_first_categories(data: dict, is_author: bool, name_dict: dict):
    other_type_display = "パズル" if is_author else "作者"
    image_name = "first-puzzles-by-author.png" if is_author else "first-authors-by-puzzle.png"

    pyplot.rcParams["font.family"] = 'MotoyaLMaru'
    fig = pyplot.figure(figsize=[8, 20])
    ax = pyplot.axes()
    ax.set_axisbelow(True)
    ax.tick_params(width=0, which="both")
    pyplot.subplot().margins(0.05, 0.005)
    pyplot.grid(axis="x", which="both", c="grey")
    pyplot.subplots_adjust(left=0.28, right=0.99, top=0.97, bottom=0.03)

    pyplot.title("初投稿した" + other_type_display + "の数")
    pyplot.ylabel("")
    pyplot.xlabel(other_type_display + "の数")

    x, y = get_first_categories(data, is_author, name_dict)
    pyplot.barh(x, y, color="green")
    fig.savefig("graph/" + image_name)


def main():
    data = load("data/data.json")
    user_data = load("data/user.json")
    kind_data = load("data/kind.json")

    plot_first_categories(data, True, user_data)
    plot_first_categories(data, False, kind_data)
    return


if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*- #
import json
from datetime import datetime
from matplotlib import pyplot


def load(file: str):
    with open(file, encoding='utf8') as f:
        data_json = f.read()
        return json.loads(data_json)


def get_span_categories(data: dict, is_author: bool, limit: int, categories: dict):
    category_id = "user" if is_author else "kind"

    problem_dict = {}
    for d in data.values():
        time = datetime.fromisoformat(d["registered"])
        id_str = str(d[category_id])
        name = categories[id_str]["name"]
        if id_str not in problem_dict:
            problem_dict[id_str] = {"first": time, "last": time, "count": 1, "name": name, "id": id_str}
        else:
            if problem_dict[id_str]["first"] > time:
                problem_dict[id_str]["first"] = time
            if problem_dict[id_str]["last"] < time:
                problem_dict[id_str]["last"] = time
            problem_dict[id_str]["count"] += 1

    sorted_list = sorted(problem_dict.values(), key=lambda x: x["count"])
    limited_list = sorted_list[-1 * limit:]

    names = [p["name"] for p in limited_list]
    firsts = [p["first"] for p in limited_list]
    lasts = [p["last"] for p in limited_list]

    # 同名アカウントがあるときは id を付けて区別する
    if category_id == 'user':
        duplicated_names = []
        for name in names:
            if name in duplicated_names:
                continue
            if names.count(name) > 1:
                duplicated_names.append(name)
        for name_iter, name in enumerate(names):
            if name in duplicated_names:
                id_str = limited_list[name_iter]["id"]
                name += ' (' + id_str + ')'
                names[name_iter] = name

    return names, firsts, lasts


def plot_span_categories(data: dict, is_author: bool, categories: dict):
    limit = 100
    name_display = "作者" if is_author else "パズル"
    image_name = "span-by-author.png" if is_author else "span-by-puzzle.png"

    pyplot.rcParams["font.family"] = 'MotoyaLMaru'
    fig = pyplot.figure(figsize=[8, 20])
    ax = pyplot.axes()
    ax.set_axisbelow(False)
    ax.tick_params(width=0, which="both")
    pyplot.subplot().margins(0.05, 0.005)
    pyplot.grid(axis="x", which="both", c="grey")
    pyplot.subplots_adjust(left=0.25, right=0.97, top=0.97, bottom=0.03)
    pyplot.xlim(datetime.fromisoformat("2019-05-01 00:00:00"), datetime.today())

    pyplot.title(name_display + "別投稿期間（最古の問題～最新の問題／投稿数上位" + str(limit) + "）")
    pyplot.ylabel("")
    pyplot.xlabel("")

    x, y1, y2 = get_span_categories(data, is_author, limit, categories)
    pyplot.barh(x, y2, color="green", height=0.4)
    pyplot.barh(x, y1, color="white", height=0.4)
    fig.savefig("graph/" + image_name)


def main():
    data = load("data/data.json")
    user_data = load("data/user.json")
    kind_data = load("data/kind.json")
    plot_span_categories(data, True, user_data)
    plot_span_categories(data, False, kind_data)
    return


if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*- #
import json
from datetime import datetime
from matplotlib import pyplot

def load(file: str):
    with open(file, encoding='utf8') as f:
        data_json = f.read()
        return json.loads(data_json)


def get_span_categories(data: dict, is_author: bool, limit: int):
    category_name = "author_name" if is_author else "puzzle_name"

    problem_dict = {}
    for d in data:
        time = datetime.fromisoformat(d["created_at"])
        name = d[category_name]
        if name not in problem_dict:
            problem_dict[name] = {"first": time, "last": time, "count": 1}
        else:
            if problem_dict[name]["first"] > time:
                problem_dict[name]["first"] = time
            if problem_dict[name]["last"] < time:
                problem_dict[name]["last"] = time
            problem_dict[name]["count"] += 1

    del_list = []
    for name, p in problem_dict.items():
        if p["count"] < limit:
            del_list.append(name)
    for name in del_list:
        del problem_dict[name]
    sorted_dict = sorted(problem_dict.items(), key=lambda x: x[1]["count"])

    names = [name for name, _ in sorted_dict]
    firsts = [p["first"] for _, p in sorted_dict]
    lasts = [p["last"] for _, p in sorted_dict]

    return names, firsts, lasts


def plot_span_categories(data: dict, is_author: bool):
    limit = 20
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

    pyplot.title(name_display + "別投稿期間（最古の問題～最新の問題／投稿数" + str(limit) + "以上）")
    pyplot.ylabel("")
    pyplot.xlabel("")

    x, y1, y2 = get_span_categories(data, is_author, limit)
    pyplot.barh(x, y2, color="blue", height=0.4)
    pyplot.barh(x, y1, color="white", height=0.4)
    fig.savefig("graph/" + image_name)


def main():
    data = load("data/data.json")
    plot_span_categories(data, True)
    plot_span_categories(data, False)
    return


if __name__ == '__main__':
    main()
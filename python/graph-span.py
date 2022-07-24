# -*- coding: utf-8 -*- #
from itertools import count
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
            problem_dict[name] = {"first": time, "last": time, "count": 1, "name": name}
        else:
            if problem_dict[name]["first"] > time:
                problem_dict[name]["first"] = time
            if problem_dict[name]["last"] < time:
                problem_dict[name]["last"] = time
            problem_dict[name]["count"] += 1

    sorted_list = sorted(problem_dict.values(), key=lambda x:x["count"])
    limited_list = sorted_list[-1*limit:]

    names = [p["name"] for p in limited_list]
    firsts = [p["first"] for p in limited_list]
    lasts = [p["last"] for p in limited_list]

    return names, firsts, lasts


def plot_span_categories(data: dict, is_author: bool):
    limit = 50
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

    x, y1, y2 = get_span_categories(data, is_author, limit)
    pyplot.barh(x, y2, color="green", height=0.4)
    pyplot.barh(x, y1, color="white", height=0.4)
    fig.savefig("graph/" + image_name)


def main():
    data = load("data/data.json")
    plot_span_categories(data, True)
    plot_span_categories(data, False)
    return


if __name__ == '__main__':
    main()
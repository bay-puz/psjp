# -*- coding: utf-8 -*- #
import json
from datetime import datetime
from matplotlib import pyplot

def load(file: str):
    with open(file, encoding='utf8') as f:
        data_json = f.read()
        return json.loads(data_json)


def get_first_list(data: dict, is_author: bool):
    data_name = "author_name" if is_author else "puzzle_name"
    first_problem = {}
    for d in data:
        name = d[data_name]
        time = datetime.fromisoformat(d["created_at"]).strftime("%Y-%m")
        if name in first_problem:
            if first_problem[name] > time:
                first_problem[name] = time
        else:
            first_problem[name] = time

    times = []
    count = []
    for name, time in first_problem.items():
        if time in times:
            count[times.index(time)] += 1
        else:
            times.append(time)
            count.append(1)

    return times, count


def plot_first_time(data: dict, is_author: bool):
    type_display = "作者" if is_author else "パズル"
    image_name = "first-author-count.png" if is_author else "first-puzzle-count.png"

    pyplot.rcParams["font.family"] = 'MotoyaLMaru'
    fig = pyplot.figure(figsize=[14, 7])
    ax = pyplot.axes()
    ax.set_axisbelow(True)
    ax.tick_params(width=0, which="both")
    pyplot.subplot().margins(0.01, 0.05)
    pyplot.grid(axis="y", which="both", c="grey")
    pyplot.xticks(rotation=50)

    pyplot.title("始投稿の" + type_display + "の数")
    pyplot.xlabel("年/月")
    pyplot.ylabel(type_display + "数")

    x, y = get_first_list(data, is_author)
    pyplot.plot(x, y, color="green")
    fig.savefig("graph/" + image_name)


def main():
    data = load("data/data.json")
    plot_first_time(data, True)
    plot_first_time(data, False)
    return


if __name__ == '__main__':
    main()
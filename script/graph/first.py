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
        name = name_dict[str(d[category])]["name"]
        if category_id in first_problem:
            if first_problem[category_id]["time"] > time:
                first_problem[category_id]["time"] = time
                first_problem[category_id]["name"] = name
        else:
            first_problem[category_id] = {"time": time, "name": name}

    counts_dict = {}
    for d in first_problem.values():
        name = d["name"]
        if name in counts_dict:
            counts_dict[name] += 1
        else:
            counts_dict[name] = 1

    sorted_dict = sorted(counts_dict.items(), key=lambda x: x[1])
    names = [name for name, _ in sorted_dict]
    counts = [count for _, count in sorted_dict]

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


def get_first_month(data: dict, is_author: bool, name_dict: dict):
    search_id = "user" if is_author else "kind"
    first_problem = {}
    for d in data.values():
        category_id = d[search_id]
        time = datetime.fromisoformat(d["registered"]).strftime("%Y-%m")
        name = name_dict[str(category_id)]["name"]
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


def plot_first_month(data: dict, is_author: bool, name_dict: dict):
    type_display = "作者" if is_author else "パズル"
    image_name = "first-month-author.png" if is_author else "first-month-puzzle.png"

    pyplot.rcParams["font.family"] = 'MotoyaLMaru'
    fig = pyplot.figure(figsize=[14, 7])
    ax = pyplot.axes()
    ax.set_axisbelow(True)
    ax.tick_params(width=0, which="both")
    pyplot.subplot().margins(0.01, 0.05)
    pyplot.grid(axis="y", which="both", c="grey")
    pyplot.xticks(rotation=50)

    pyplot.title("初投稿の" + type_display + "の数")
    pyplot.xlabel("")
    pyplot.ylabel(type_display + "数")

    x, y = get_first_month(data, is_author, name_dict)
    pyplot.plot(x, y, color="green")
    fig.savefig("graph/" + image_name)


def main():
    data = load("data/data.json")
    user_data = load("data/user.json")
    kind_data = load("data/kind.json")
    plot_first_month(data, True, user_data)
    plot_first_month(data, False, kind_data)

    plot_first_categories(data, True, user_data)
    plot_first_categories(data, False, kind_data)
    return


if __name__ == '__main__':
    main()
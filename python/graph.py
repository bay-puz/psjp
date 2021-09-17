# -*- coding: utf-8 -*- #
import json
from matplotlib import pyplot


def load(file: str):
    with open(file, encoding='utf8') as f:
        data_json = f.read()
        return json.loads(data_json)


def problem_liked_by(data_dict: dict):
    problem_list = []
    liked_list = []
    for data in data_dict.values():
        problem_list.append(data["problem"])
        liked_list.append(data["liked"])
    return problem_list, liked_list


def plot_problem_liked_by(author_dict, puzzle_dict):
    pyplot.rcParams["font.family"] = 'MotoyaLMaru'
    fig = pyplot.figure()

    pyplot.xlabel("問題数")
    pyplot.ylabel("いいね数")
    pyplot.xscale("log")
    pyplot.yscale("log")

    x, y = problem_liked_by(author_dict)
    pyplot.title("作者別問題数/いいね数")
    pyplot.scatter(x, y, s=5, c='g')
    fig.savefig("graph/problem-liked-by-author.png")

    x, y = problem_liked_by(puzzle_dict)
    pyplot.title("パズル別問題数/いいね数")
    pyplot.scatter(x, y, s=5, c='g')
    fig.savefig("graph/problem-liked-by-puzzle.png")
    return


def top_in_problem(data_dict: dict, type: str, limit: int):
    labels = []
    width_top = []
    width_other = []

    def sort_problem(d):
        return int(d["problem"])

    sorted_list = sorted(data_dict.values(), key=sort_problem)
    limit_list = sorted_list[-1*limit:]

    for data in limit_list:
        labels.append(data["name"])

        max_problem = 0
        for d in data[type].values():
            p = int(d["problem"])
            if p > max_problem:
                max_problem = p
        p = int(data["problem"])
        width_top.append(p)
        width_other.append(p - max_problem)

    return labels, width_top, width_other


def plot_top_in_problem(author_dict, puzzle_dict):
    pyplot.rcParams["font.family"] = 'MotoyaLMaru'
    size = 50

    def set_plot():
        ax = pyplot.axes()
        pyplot.xlabel("問題数")
        pyplot.ylabel("")
        pyplot.xscale("linear")
        pyplot.yscale("linear")
        pyplot.minorticks_on()
        ax.set_axisbelow(True)
        ax.tick_params(width=0, which="both")
        pyplot.grid(axis="x", which="both", c="grey", alpha=0.5)
        pyplot.subplots_adjust(left=0.25, right=0.95, bottom=0.05, top=0.95)
        pyplot.subplot().margins(0.02, 0.01)

    fig = pyplot.figure(figsize=[10, 12])
    set_plot()
    l, t, o = top_in_problem(puzzle_dict, "author", size)
    pyplot.title("パズル別総問題数/最多投稿者の問題数（問題数上位" + str(size) + "）")
    pyplot.barh(l, t, fc="orange", label="そのパズルの最多投稿者")
    pyplot.barh(l, o, fc="green", label="他の投稿者の合計")
    pyplot.legend()
    fig.savefig("graph/problem-by-puzzle.png")

    fig = pyplot.figure(figsize=[10, 12])
    set_plot()
    l, t, o = top_in_problem(author_dict, "puzzle", size)
    pyplot.title("作者別総投稿数/最多投稿パズルの投稿数（投稿数上位" + str(size) + "）")
    pyplot.barh(l, t, fc="orange", label="その作者の最多パズル")
    pyplot.barh(l, o, fc="green", label="それ以外のパズルの合計")
    pyplot.legend()
    fig.savefig("graph/problem-by-author.png")

    return


def main():
    data_author = load("data/author.json")
    data_puzzle = load("data/puzzle.json")

    del data_author["全作者"]
    del data_puzzle["全パズル"]

    plot_problem_liked_by(data_author, data_puzzle)
    plot_top_in_problem(data_author, data_puzzle)

    return

if __name__ == '__main__':
    main()
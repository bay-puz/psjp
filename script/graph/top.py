# -*- coding: utf-8 -*- #
import json
from matplotlib import pyplot


def load(file: str):
    with open(file, encoding='utf8') as f:
        data_json = f.read()
        return json.loads(data_json)


def top(data_dict: dict, name_dict: dict, type: str, limit: int):
    labels = []
    width_top = []
    width_other = []

    def sort_problem(d):
        return int(d["problem_n"])

    sorted_list = sorted(data_dict.values(), key=sort_problem)
    limit_list = sorted_list[-1 * limit:]

    label_ids = []
    for data in limit_list:
        id_str = str(data["id"])
        label_ids.append(id_str)

        max_problem = 0
        for d in data[type].values():
            p = int(d["problem_n"])
            if p > max_problem:
                max_problem = p
        p = int(data["problem_n"])
        width_top.append(p)
        width_other.append(p - max_problem)

    labels = [name_dict[id_str]["name"] for id_str in label_ids]

    # 同名アカウントがあるときは id を付けて区別する
    duplicated_names = []
    for name in labels:
        if name in duplicated_names:
            continue
        if labels.count(name) > 1:
            duplicated_names.append(name)
    print(duplicated_names)
    for name_iter, name in enumerate(labels):
        if name in duplicated_names:
            id_str = label_ids[name_iter]
            name += ' (' + id_str + ')'
            labels[name_iter] = name

    return labels, width_top, width_other


def plot(author_dict, puzzle_dict, user_dict, kind_dict):
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
        pyplot.subplots_adjust(left=0.28, right=0.95, bottom=0.05, top=0.95)
        pyplot.subplot().margins(0.02, 0.01)

    fig = pyplot.figure(figsize=[8, 12])
    set_plot()
    l, t, o = top(puzzle_dict, kind_dict, "author", size)
    pyplot.title("パズル別総問題数/最多投稿者の問題数（問題数上位" + str(size) + "）")
    pyplot.barh(l, t, fc="orange", label="そのパズルの最多投稿者")
    pyplot.barh(l, o, fc="green", label="他の投稿者の合計")
    pyplot.legend()
    fig.savefig("graph/problem-by-puzzle.png")

    fig = pyplot.figure(figsize=[8, 12])
    set_plot()
    l, t, o = top(author_dict, user_dict, "kind", size)
    pyplot.title("作者別総投稿数/最多投稿パズルの投稿数（投稿数上位" + str(size) + "）")
    pyplot.barh(l, t, fc="orange", label="その作者の最多パズル")
    pyplot.barh(l, o, fc="green", label="それ以外のパズルの合計")
    pyplot.legend()
    fig.savefig("graph/problem-by-author.png")


def main():
    data_author = load("data/author.json")
    data_user = load("data/user.json")
    data_puzzle = load("data/puzzle.json")
    data_kind = load("data/kind.json")

    del data_author["0"]
    del data_puzzle["0"]

    plot(data_author, data_puzzle, data_user, data_kind)


if __name__ == '__main__':
    main()

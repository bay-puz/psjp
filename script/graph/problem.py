# -*- coding: utf-8 -*- #
import json
from matplotlib import pyplot


def load(file: str):
    with open(file, encoding='utf8') as f:
        data_json = f.read()
        return json.loads(data_json)


def count_problem(data_dict: dict):
    problem_list = []
    favorite_list = []
    answered_list = []
    for data in data_dict.values():
        problem_list.append(data["problem_n"])
        favorite_list.append(data["favorite_n"])
        answered_list.append(data["answered_n"])
    return problem_list, favorite_list, answered_list


def plot(x, y, is_author, is_fav):
    category = "作者" if is_author else "パズル"
    label = "いいね" if is_fav else "被解答登録"
    pyplot.rcParams["font.family"] = 'MotoyaLMaru'
    fig = pyplot.figure()

    pyplot.xlabel("問題数")
    pyplot.ylabel(f"{label}数")
    pyplot.xscale("log")
    pyplot.yscale("log")

    pyplot.title(f"{category}別問題数/{label}数")
    pyplot.scatter(x, y, s=5, c='g')
    category_en = "author" if is_author else "puzzle"
    label_en = "favorite" if is_fav else "answered"
    fig.savefig(f"graph/problem-{label_en}-{category_en}.png")


def plot_problem(author_dict, puzzle_dict):
    p, f, a = count_problem(author_dict)
    plot(p, f, is_author=True, is_fav=True)
    plot(p, a, is_author=True, is_fav=False)

    p, f, a = count_problem(puzzle_dict)
    plot(p, f, is_author=False, is_fav=True)
    plot(p, a, is_author=False, is_fav=False)


def main():
    data_author = load("data/author.json")
    data_puzzle = load("data/puzzle.json")

    del data_author["0"]
    del data_puzzle["0"]

    plot_problem(data_author, data_puzzle)


if __name__ == '__main__':
    main()

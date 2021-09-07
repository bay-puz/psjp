# -*- coding: utf-8 -*- #
import json
from matplotlib import colors, pyplot


def problem_liked_by(data_dict: dict):
    problem_list = []
    liked_list = []
    for data in data_dict.values():
        problem_list.append(data["problem"])
        liked_list.append(data["liked"])
    return problem_list, liked_list


def load(file: str):
    with open(file, encoding='utf8') as f:
        data_json = f.read()
        return json.loads(data_json)


def main():
    data_author = load("../data/authors.json")
    data_puzzle = load("../data/puzzles.json")

    pyplot.rcParams["font.family"] = 'MotoyaLMaru'
    fig = pyplot.figure()

    pyplot.xlabel("問題数")
    pyplot.ylabel("いいね数")
    pyplot.xscale("log")
    pyplot.yscale("log")

    x, y = problem_liked_by(data_author)
    pyplot.title("作者別問題数/いいね数")
    pyplot.scatter(x, y, s=5, c='g')
    fig.savefig("../graph/problem-liked_by_author.png")

    x, y = problem_liked_by(data_puzzle)
    pyplot.title("パズル別問題数/いいね数")
    pyplot.scatter(x, y, s=5, c='g')
    fig.savefig("../graph/problem-liked_by_puzzle.png")

    return

if __name__ == '__main__':
    main()